# Epic Date Format - Clarification

## ✅ Epic Standard Format (Supported by Epic Real API)

Epic FHIR API **ONLY** supports standard FHIR date prefixes:

### Standard Epic Formats:
```bash
# Exact date
GET /Appointment?date=eq2025-01-15

# On or after date
GET /Appointment?date=ge2025-01-15

# On or before date
GET /Appointment?date=le2025-01-15

# After date (greater than)
GET /Appointment?date=gt2025-01-15

# Before date (less than)
GET /Appointment?date=lt2025-01-15
```

### For Today's Appointments in Epic:
Since Epic doesn't support `date=today`, you need to use:

```bash
# Option 1: Exact date (today's date)
GET /Appointment?date=eq2025-01-15

# Option 2: Date range (today's date range)
GET /Appointment?date=ge2025-01-15&date=le2025-01-15
```

## ⚠️ Our Convenience Feature

`date=today` is **NOT** Epic standard - it's our convenience feature.

**In Real Epic API:**
- ❌ `date=today` - **NOT SUPPORTED**
- ✅ `date=eqYYYY-MM-DD` - **SUPPORTED**
- ✅ `date=geYYYY-MM-DD` - **SUPPORTED**
- ✅ `date=leYYYY-MM-DD` - **SUPPORTED**
- ✅ `date=gtYYYY-MM-DD` - **SUPPORTED**
- ✅ `date=ltYYYY-MM-DD` - **SUPPORTED**

## Our Implementation

Our API supports **BOTH**:
1. ✅ Epic standard formats (ge, le, gt, lt, eq) - **Epic Compatible**
2. ⚠️ Convenience feature (`date=today`) - **NOT Epic Standard, but works in our mock**

## Recommendation

For **Epic compatibility**, use:
```bash
# Today's appointments (use actual date)
GET /Appointment?date=eq2025-01-15

# Or date range
GET /Appointment?date=ge2025-01-15&date=le2025-01-15
```

**Don't use** `date=today` when connecting to real Epic API - it won't work!

## Summary

| Format | Epic Real API | Our Mock API | Status |
|--------|--------------|--------------|--------|
| `date=eq2025-01-15` | ✅ Supported | ✅ Supported | ✅ Epic Standard |
| `date=ge2025-01-15` | ✅ Supported | ✅ Supported | ✅ Epic Standard |
| `date=le2025-01-15` | ✅ Supported | ✅ Supported | ✅ Epic Standard |
| `date=gt2025-01-15` | ✅ Supported | ✅ Supported | ✅ Epic Standard |
| `date=lt2025-01-15` | ✅ Supported | ✅ Supported | ✅ Epic Standard |
| `date=today` | ❌ NOT Supported | ✅ Supported | ⚠️ Convenience Only |

## Conclusion

✅ **Our API fully supports Epic standard date formats**  
⚠️ **`date=today` is convenience only - not Epic standard**  
✅ **Use Epic standard formats for real Epic API integration**

