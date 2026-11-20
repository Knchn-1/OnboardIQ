"""
Automated Test Suite for Reference Authorizer & Fail-Closed Behavior
Tests:
  - Positive authorization (authorized roles)
  - Negative rejection (unauthorized roles)
  - Restricted unit access tests (RU-001, RU-002, RU-003)
  - Leak detection tests
  - Fail-closed edge cases (unknown principal, malformed metadata, empty groups, attacker bypass)
"""
import json
import os
from reference_authorizer import ReferenceAuthorizer

def run_tests():
    auth = ReferenceAuthorizer()
    results = []
    
    def log_test(test_id, description, expected, actual, passed, details=""):
        results.append({
            "test_id": test_id,
            "description": description,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "details": details
        })

    # Test 1: Standard employee accesses ALL_EMPLOYEES chunk
    chunk_general = {
        "classification_audience": "ALL_EMPLOYEES",
        "allowed_groups": ["GRP_ALL_EMPLOYEES"],
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-007", chunk_general)
    log_test("TC-AC-001", "Vikram Joshi (ENG) accesses ALL_EMPLOYEES content", True, allowed, allowed == True, reason)

    # Test 2: Standard employee accesses RU-001 (HR_ONLY) -> MUST DENY
    chunk_ru1 = {
        "classification_audience": "HR_ONLY",
        "allowed_groups": ["GRP_DEPT_HR"],
        "restricted_unit_id": "RU-001",
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-007", chunk_ru1)
    log_test("TC-AC-002", "Vikram Joshi (ENG) accesses RU-001 (HR Disciplinary)", False, allowed, allowed == False, reason)

    # Test 3: HR employee accesses RU-001 (HR_ONLY) -> MUST ALLOW
    allowed, reason = auth.authorize_chunk("EMP-002", chunk_ru1)
    log_test("TC-AC-003", "Ishita Rao (HR) accesses RU-001 (HR Disciplinary)", True, allowed, allowed == True, reason)

    # Test 4: Data Analyst accesses RU-002 (IT Incident Playbook IT_ONLY) -> MUST DENY
    chunk_ru2 = {
        "classification_audience": "IT_ONLY",
        "allowed_groups": ["GRP_DEPT_IT"],
        "restricted_unit_id": "RU-002",
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-010", chunk_ru2)
    log_test("TC-AC-004", "Sana Khan (DA) accesses RU-002 (IT Incident Playbook)", False, allowed, allowed == False, reason)

    # Test 5: IT Manager accesses RU-002 -> MUST ALLOW
    allowed, reason = auth.authorize_chunk("EMP-004", chunk_ru2)
    log_test("TC-AC-005", "Neha Kulkarni (IT) accesses RU-002 (IT Incident Playbook)", True, allowed, allowed == True, reason)

    # Test 6: Sales Manager accesses RU-003 (Finance Fraud Controls FINANCE_ONLY) -> MUST DENY
    chunk_ru3 = {
        "classification_audience": "FINANCE_ONLY",
        "allowed_groups": ["GRP_DEPT_FIN"],
        "restricted_unit_id": "RU-003",
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-013", chunk_ru3)
    log_test("TC-AC-006", "Rahul Sethi (SCS) accesses RU-003 (Finance Audit Controls)", False, allowed, allowed == False, reason)

    # Test 7: Finance Manager accesses RU-003 -> MUST ALLOW
    allowed, reason = auth.authorize_chunk("EMP-011", chunk_ru3)
    log_test("TC-AC-007", "Arjun Bhat (FIN) accesses RU-003 (Finance Audit Controls)", True, allowed, allowed == True, reason)

    # Test 8: Non-manager accesses MANAGERS document (NST-HR-POL-007) -> MUST DENY
    chunk_mgr = {
        "classification_audience": "MANAGERS_AND_HR",
        "allowed_groups": ["GRP_MANAGERS", "GRP_DEPT_HR"],
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-008", chunk_mgr)
    log_test("TC-AC-008", "Mira Nair (SWE, Non-Manager) accesses Performance/Promotion Policy", False, allowed, allowed == False, reason)

    # Test 9: Engineering Manager accesses MANAGERS document -> MUST ALLOW
    allowed, reason = auth.authorize_chunk("EMP-006", chunk_mgr)
    log_test("TC-AC-009", "Ananya Iyer (Engineering Manager) accesses Performance/Promotion Policy", True, allowed, allowed == True, reason)

    # Test 10: Fail-closed on Unknown/Synthetic Principal -> MUST DENY
    allowed, reason = auth.authorize_chunk("EMP-999-ATTACKER", chunk_general)
    log_test("TC-AC-010", "Unregistered Principal (EMP-999) accesses public content", False, allowed, allowed == False, reason)

    # Test 11: Fail-closed on None/Missing Principal -> MUST DENY
    allowed, reason = auth.authorize_chunk(None, chunk_general)
    log_test("TC-AC-011", "Missing Principal (None) accesses content", False, allowed, allowed == False, reason)

    # Test 12: Fail-closed on Empty allowed_groups -> MUST DENY
    chunk_corrupt1 = {
        "classification_audience": "ALL_EMPLOYEES",
        "allowed_groups": [],
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-001", chunk_corrupt1)
    log_test("TC-AC-012", "Corrupt metadata with empty allowed_groups", False, allowed, allowed == False, reason)

    # Test 13: Fail-closed on Invalid Group Name -> MUST DENY
    chunk_corrupt2 = {
        "classification_audience": "ALL_EMPLOYEES",
        "allowed_groups": ["GRP_SUPERADMIN_INVENTED"],
        "access_policy_version": "v1.0"
    }
    allowed, reason = auth.authorize_chunk("EMP-001", chunk_corrupt2)
    log_test("TC-AC-013", "Corrupt metadata with invented group name", False, allowed, allowed == False, reason)

    # Test 14: Fail-closed on Stale Policy Version -> MUST DENY
    chunk_stale = {
        "classification_audience": "ALL_EMPLOYEES",
        "allowed_groups": ["GRP_ALL_EMPLOYEES"],
        "access_policy_version": "v0.9_REVOKED"
    }
    allowed, reason = auth.authorize_chunk("EMP-001", chunk_stale)
    log_test("TC-AC-014", "Stale/revoked policy version chunk", False, allowed, allowed == False, reason)

    # Test 15: Database Filter Clause Generation Check
    db_clause_eng = auth.build_db_filter_clause("EMP-007")
    expected_clause_part = "'GRP_ALL_EMPLOYEES'"
    is_valid_db = expected_clause_part in db_clause_eng and "'GRP_DEPT_ENG'" in db_clause_eng
    log_test("TC-AC-015", "SQL pre-query filter generation for ENG employee", True, is_valid_db, is_valid_db, db_clause_eng)

    # Test 16: Database Filter Clause for Attacker -> WHERE 1 = 0
    db_clause_fake = auth.build_db_filter_clause("FAKE-USER")
    log_test("TC-AC-016", "SQL pre-query filter for unauthenticated user", "WHERE 1 = 0", db_clause_fake, db_clause_fake == "WHERE 1 = 0", db_clause_fake)

    # Save results
    os.makedirs("knowledge_base/06_verification", exist_ok=True)
    summary = {
        "total_tests": len(results),
        "passed_tests": sum(1 for r in results if r["passed"]),
        "failed_tests": sum(1 for r in results if not r["passed"]),
        "status": "PASS" if all(r["passed"] for r in results) else "FAIL",
        "test_results": results
    }
    
    with open("knowledge_base/06_verification/authorizer_test_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print(f"Authorizer tests finished: {summary['passed_tests']}/{summary['total_tests']} PASSED.")
    return summary["status"] == "PASS"

if __name__ == "__main__":
    run_tests()

