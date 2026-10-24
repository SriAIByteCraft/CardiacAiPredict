# Automated Software Testing Report

**Testing Framework**: `pytest 8.x`  
**Test Suite Path**: `backend/tests/`  
**Test Client**: Flask Test Client  
**Database Test Store**: `mongomock` in-memory collection isolation  

---

## 1. Test Execution Summary

```
============================= 24 passed in 2.86s ==============================
```

- **Total Test Cases**: 24
- **Passed**: 24 (100%)
- **Failed**: 0
- **Errors**: 0

---

## 2. Test Cases Breakdown

### Authentication & Session Security (`backend/tests/test_auth.py`)
1. `test_register_success`: Verifies new account creation, password hashing, and exclusion of sensitive hash in response.
2. `test_register_duplicate_email`: Verifies unique index enforcement and 409 Conflict rejection for duplicate emails.
3. `test_register_weak_password`: Verifies rejection of passwords under 8 characters or lacking required digits/letters.
4. `test_login_success`: Verifies session initialization upon valid credential submission.
5. `test_login_invalid_password`: Verifies 401 Unauthorized rejection for incorrect passwords.
6. `test_unauthenticated_me`: Verifies unauthenticated visitors cannot access `/api/auth/me`.
7. `test_logout`: Verifies cookie clearing and session invalidation.

### Profile Management (`backend/tests/test_profile.py`)
8. `test_get_profile`: Verifies retrieval of sanitized user profile details.
9. `test_update_profile`: Verifies updating clinician display name.
10. `test_change_password_success`: Verifies password update and new hash computation.
11. `test_change_password_wrong_current`: Verifies rejection when current password verification fails.

### Machine Learning & Prediction Validation (`backend/tests/test_predictions.py`)
12. `test_predict_unauthenticated`: Verifies 401 response when attempting inference without logging in.
13. `test_predict_invalid_schema_missing_fields`: Verifies 400 rejection when required features are omitted.
14. `test_predict_out_of_bounds`: Verifies 400 rejection when numeric values violate biological boundaries (e.g. Age > 100).
15. `test_predict_invalid_category`: Verifies 400 rejection when categorical attributes have invalid integers (e.g. sex = 9).
16. `test_predict_success_and_persistence`: Verifies end-to-end inference through the fitted StackingClassifier pipeline and automated database record creation.

### Prediction History & Isolation (`backend/tests/test_history.py`)
17. `test_history_unauthenticated`: Verifies 401 response for unauthenticated history requests.
18. `test_history_empty_state`: Verifies safe handling and pagination response when user has zero records.
19. `test_history_user_isolation`: **Critical Security Test**: Verifies that User A cannot view User B's prediction records or query them by direct ID.
20. `test_dashboard_stats`: Verifies aggregation of total counts, risk tier breakdowns, and 7-day timeline.

### Validators & Diagnostics (`backend/tests/test_validators.py`)
21. `test_email_validation`: Verifies RFC email regex validator.
22. `test_password_strength`: Verifies minimum length, letter, and number policy.
23. `test_health_endpoint`: Verifies `/api/health` diagnostic endpoint.
24. `test_database_health_endpoint`: Verifies `/api/database-health` diagnostic endpoint.
