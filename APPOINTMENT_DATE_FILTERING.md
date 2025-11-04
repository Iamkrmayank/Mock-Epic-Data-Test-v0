# Appointment Date Filtering - Epic Compatible

## Overview

Epic FHIR API supports date filtering for appointments. You can filter appointments by:
- **Today's appointments** - Use `date=today`
- **Date range** - Use FHIR date prefixes (ge, le, gt, lt, eq)
- **Specific date** - Use exact date or partial date

## Supported Date Formats

### 1. Today's Appointments

Get all appointments for today:

```bash
GET /Appointment?date=today
```

Or with patient filter:

```bash
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=today
```

### 2. FHIR Date Prefixes

Epic supports FHIR standard date prefixes:

- **`ge`** (greater than or equal) - Appointments on or after this date
- **`le`** (less than or equal) - Appointments on or before this date
- **`gt`** (greater than) - Appointments after this date
- **`lt`** (less than) - Appointments before this date
- **`eq`** (equals) - Appointments on this exact date

#### Examples:

```bash
# Appointments on or after 2025-01-01
GET /Appointment?date=ge2025-01-01

# Appointments on or before 2025-12-31
GET /Appointment?date=le2025-12-31

# Appointments between dates (combine with other filters)
GET /Appointment?date=ge2025-01-01&date=le2025-12-31

# Appointments on exact date
GET /Appointment?date=eq2025-11-05

# Appointments after today
GET /Appointment?date=gt2025-01-15
```

### 3. Partial Date Matching

You can also use partial dates for month or year filtering:

```bash
# All appointments in November 2025
GET /Appointment?date=2025-11

# All appointments in 2025
GET /Appointment?date=2025
```

### 4. Combined Filters

Combine date with other filters:

```bash
# Today's booked appointments for a patient
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=today&status=booked

# Upcoming appointments (on or after today)
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=ge2025-01-15&status=booked

# Past appointments (before today)
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=lt2025-01-15
```

## Real-World Examples

### Get Today's Schedule

```bash
GET /Appointment?date=today&status=booked
```

### Get This Week's Appointments

```bash
# Get appointments from today onwards
GET /Appointment?date=ge2025-01-15&status=booked
```

### Get Past Appointments

```bash
# Get appointments before today
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=lt2025-01-15
```

### Get Appointments for Specific Date

```bash
GET /Appointment?date=eq2025-11-05
```

## Response Format

All date-filtered searches return the same Bundle format:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 5,
  "entry": [
    {
      "fullUrl": "https://fhir.epic.com/.../Appointment/{id}",
      "resource": {
        "resourceType": "Appointment",
        "id": "...",
        "start": "2025-11-05T14:00:00Z",
        "end": "2025-11-05T15:30:00Z",
        "status": "booked",
        ...
      },
      "search": {"mode": "match"}
    }
  ]
}
```

## Epic Compatibility

This implementation matches Epic's FHIR R4 Appointment API date filtering:

✅ Supports `date=today` for today's appointments  
✅ Supports FHIR date prefixes (ge, le, gt, lt, eq)  
✅ Supports partial date matching  
✅ Works with other filters (patient, status, actor)  
✅ Returns Epic-compatible Bundle format  

## Testing

### Test Today's Appointments

```bash
# Start server
python fhir_api.py

# Test today's appointments
curl "http://localhost:8000/Appointment?date=today"

# Test with patient filter
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=today"
```

### Test Date Ranges

```bash
# Appointments on or after date
curl "http://localhost:8000/Appointment?date=ge2025-01-01"

# Appointments on exact date
curl "http://localhost:8000/Appointment?date=eq2025-11-05"
```

## Notes

- Date comparisons are done at the **date level** (not time level)
- `date=today` uses the server's current date
- All dates are in ISO 8601 format (YYYY-MM-DD)
- Timezone handling follows Epic's pattern (UTC)

