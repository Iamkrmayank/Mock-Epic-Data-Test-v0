"""
Test Epic FHIR API endpoints
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, method="GET", expected_status=200):
    """Test an API endpoint"""
    try:
        print(f"\n{name}...")
        response = requests.request(method, url, timeout=5)
        
        if response.status_code == expected_status:
            print(f"   [OK] Status: {response.status_code}")
            data = response.json()
            
            # Check for Bundle structure
            if isinstance(data, dict) and data.get("resourceType") == "Bundle":
                print(f"   [OK] Bundle Type: {data.get('type')}")
                print(f"   [OK] Total: {data.get('total')}")
                print(f"   [OK] Entries: {len(data.get('entry', []))}")
                if data.get('entry'):
                    first_entry = data['entry'][0]
                    print(f"   [OK] First Entry has fullUrl: {bool(first_entry.get('fullUrl'))}")
                    print(f"   [OK] First Entry has resource: {bool(first_entry.get('resource'))}")
            
            # Check for individual resource
            elif isinstance(data, dict) and data.get("resourceType"):
                print(f"   [OK] Resource Type: {data.get('resourceType')}")
                print(f"   [OK] Resource ID: {data.get('id')}")
            
            return True
        else:
            print(f"   [FAIL] Status: {response.status_code} (expected {expected_status})")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   [ERROR] Connection Error: Server not running. Start with: python fhir_api.py")
        return False
    except Exception as e:
        print(f"   [ERROR] Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Epic FHIR Mock API - Test Suite")
    print("=" * 60)
    
    # Wait for server
    print("\nWaiting for server to start...")
    time.sleep(2)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_endpoint(
        "1. Health Check",
        f"{BASE_URL}/health"
    )))
    
    # Test 2: Get Patient
    results.append(("Patient Read", test_endpoint(
        "2. Get Patient by ID",
        f"{BASE_URL}/Patient/ePtdJFCrnl2edlBDdz1C5Ja"
    )))
    
    # Test 3: Search Appointments
    results.append(("Appointment Search", test_endpoint(
        "3. Search Appointments (by patient)",
        f"{BASE_URL}/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja"
    )))
    
    # Test 4: Search Appointments by Status
    results.append(("Appointment Status Filter", test_endpoint(
        "4. Search Appointments (by status)",
        f"{BASE_URL}/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=booked"
    )))
    
    # Test 5: Search Conditions
    results.append(("Condition Search", test_endpoint(
        "5. Search Conditions (active)",
        f"{BASE_URL}/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active"
    )))
    
    # Test 6: Search Observations (with category - Epic requirement)
    results.append(("Observation Search", test_endpoint(
        "6. Search Observations (with category)",
        f"{BASE_URL}/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs&_count=2"
    )))
    
    # Test 7: Search Encounters
    results.append(("Encounter Search", test_endpoint(
        "7. Search Encounters",
        f"{BASE_URL}/Encounter?patient=ePtdJFCrnl2edlBDdz1C5Ja&_count=2"
    )))
    
    # Test 8: Search Patients by Name
    results.append(("Patient Search", test_endpoint(
        "8. Search Patients (by family name)",
        f"{BASE_URL}/Patient?family=Rodriguez"
    )))
    
    # Test 9: Search Procedures
    results.append(("Procedure Search", test_endpoint(
        "9. Search Procedures",
        f"{BASE_URL}/Procedure?patient=ePtdJFCrnl2edlBDdz1C5Ja&_count=2"
    )))
    
    # Test 10: Get Organization
    results.append(("Organization Read", test_endpoint(
        "10. Get Organization",
        f"{BASE_URL}/Organization/eLJ.EJ4jKEIQOkrtDXtBi10Q71hA1XcW9a"
    )))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! API is Epic-compliant!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
