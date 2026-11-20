"""
Reference Authorizer Implementation for OnboardIQ
Enforces strict fail-closed authorization according to specs/04_RAG_AND_ACCESS_CONTROL.md.
"""
import json

class ReferenceAuthorizer:
    def __init__(self, master_data_path="output/01_master_data/northstar_master_data.json"):
        with open(master_data_path, "r", encoding="utf-8") as f:
            self.md = json.load(f)
            
        self.employees = {e["employee_id"]: e for e in self.md["Employee_Directory_Derived"]}
        self.access_matrix = self.md["Access_Control_Matrix"]
        self.valid_groups = {
            "GRP_ALL_EMPLOYEES",
            "GRP_MANAGERS",
            "GRP_DEPT_HR",
            "GRP_DEPT_IT",
            "GRP_DEPT_ENG",
            "GRP_DEPT_DA",
            "GRP_DEPT_FIN",
            "GRP_DEPT_SCS"
        }
        self.policy_version = "v1.0"

    def resolve_principal_groups(self, employee_id):
        """Resolves active directory-derived groups for an employee ID."""
        if not employee_id or employee_id not in self.employees:
            return None  # Unauthenticated / unknown principal
        
        emp = self.employees[employee_id]
        groups = {"GRP_ALL_EMPLOYEES"}
        
        # Department group
        dept_code = emp.get("department_code")
        if dept_code in ["HR", "IT", "ENG", "DA", "FIN", "SCS"]:
            groups.add(f"GRP_DEPT_{dept_code}")
            
        # Manager group
        if emp.get("is_manager"):
            groups.add("GRP_MANAGERS")
            
        return groups

    def authorize_chunk(self, employee_id, chunk_metadata):
        """
        Evaluates authorization for an individual chunk or section.
        Returns: (is_allowed: bool, reason: str)
        Fail-closed rules strictly enforced.
        """
        # Step 1: Principal resolution
        groups = self.resolve_principal_groups(employee_id)
        if groups is None:
            return False, "DENY: Principal is missing, unknown, or unresolvable."
        
        # Step 2: Policy version check
        if chunk_metadata.get("access_policy_version", self.policy_version) != self.policy_version:
            return False, "DENY: Stale or mismatched access policy version."
            
        # Step 3: Metadata validation
        allowed_groups = chunk_metadata.get("allowed_groups")
        if not allowed_groups or not isinstance(allowed_groups, list):
            return False, "DENY: Malformed, missing, or empty allowed_groups."
            
        for g in allowed_groups:
            if g not in self.valid_groups:
                return False, f"DENY: Invalid group '{g}' detected in metadata."
                
        # Audience classification validation
        aud_label = chunk_metadata.get("classification_audience")
        if aud_label and aud_label not in self.access_matrix:
            return False, f"DENY: Unknown audience classification label '{aud_label}'."

        # Step 4: Intersection check (Any-of semantics)
        matched = set(allowed_groups).intersection(groups)
        if matched:
            return True, f"ALLOW: Authorized via matched groups: {list(matched)}"
        else:
            return False, "DENY: Principal lacks required group membership."

    def build_db_filter_clause(self, employee_id):
        """
        Generates PostgreSQL/SQL filter predicate for injection into vector & keyword queries.
        Unauthorized chunks are never scanned or retrieved.
        """
        groups = self.resolve_principal_groups(employee_id)
        if not groups:
            return "WHERE 1 = 0"  # Fail-closed
            
        group_literals = ", ".join(f"'{g}'" for g in sorted(groups))
        return f"WHERE allowed_groups && ARRAY[{group_literals}]"

