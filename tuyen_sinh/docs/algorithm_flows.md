# Tuyen Sinh — Algorithm & Data Flow Documentation

> This document describes every algorithm used in the admission processing pipeline,
> illustrated with Mermaid diagrams. All diagrams can be rendered inside VS Code with
> the "Markdown Preview Mermaid Support" extension, or on <https://mermaid.live>.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Data Model](#2-data-model)
3. [Phase 1 — Output Workbook Initialisation](#3-phase-1--output-workbook-initialisation)
4. [Phase 2 — Student Distribution](#4-phase-2--student-distribution)
5. [Phase 3 — Subject Combination (Khoi) Loading](#5-phase-3--subject-combination-khoi-loading)
6. [Phase 4 — Score Calculation](#6-phase-4--score-calculation)
   - [4a. Build Book2 Lookup](#6a-build-book2-lookup)
   - [4b. Weighted Score Formula](#6b-weighted-score-formula)
   - [4c. Priority Bonus Formula](#6c-priority-bonus-formula)
   - [4d. Per-Student Score Pipeline](#6d-per-student-score-pipeline)
7. [Phase 5 — Deduplication](#7-phase-5--deduplication)
8. [Full End-to-End Sequence](#8-full-end-to-end-sequence)
9. [Full End-to-End Activity Diagram](#9-full-end-to-end-activity-diagram)
10. [Subject Column Mapping Reference](#10-subject-column-mapping-reference)
11. [Priority Bonus Tables](#11-priority-bonus-tables)

---

## 1. System Overview

The pipeline reads three Excel input files, calculates a weighted admission score for
every applicant per major, deduplicates students who applied to multiple majors, and
writes a ranked output file.

```
┌─────────────────┐   ┌──────────────┐   ┌──────────────┐
│ toHop_THTP.xlsx │   │  Book1.xlsx  │   │  Book2.xlsx  │
│ (major ↔ khoi   │   │ (applications│   │ (exam scores │
│  mapping)       │   │  + PTXT)     │   │  + priority) │
└────────┬────────┘   └──────┬───────┘   └──────┬───────┘
         │                   │                   │
         ▼                   ▼                   ▼
    ┌────────────────────────────────────────────────┐
    │              main.py  (pipeline)               │
    │   Phase 1 → Phase 2 → Phase 3 → Phase 4 → 5   │
    └────────────────────┬───────────────────────────┘
                         │
                         ▼
               ┌──────────────────┐
               │ ExampleOutput.xlsx│
               │ one sheet/major  │
               │ sorted by score  │
               └──────────────────┘
```

---

## 2. Data Model

```mermaid
classDiagram
    class ClassKhoi {
        +str name
        +list[str] list_subject
        +dict[str,float] he_so
        +float gap_point
        +print_info()
    }

    class ClassMajor {
        +str major_id
        +list[ClassKhoi] maToHop
        +ClassKhoi primary_khoi
        +add_khoi(khoi)
        +update_primary_khoi(khoi)
        +print_info()
    }

    class ExcelHandler {
        +str name_file
        +Workbook workbook
        +Worksheet current_sheet
        +dict[str, SheetIndexMapping] listSheet
        +chosse_current_sheet(name)
        +add_sheet(name)
        +remove_sheet(name)
        +find_colum_index_with_content(content)
        +sort_inc_base_on_column_index(col)
        +remove_row_index(row)
        +remove_row_index_with_sheet(sheet, row)
        +save_file()
    }

    class SheetIndexMapping {
        +int index_colum
        +int index_row
        +int max_index_colum
        +int max_index_row
        +inc_index_column()
        +inc_index_row()
    }

    ClassMajor "1" *-- "1..*" ClassKhoi : maToHop
    ExcelHandler "1" *-- "1..*" SheetIndexMapping : listSheet
```

---

## 3. Phase 1 — Output Workbook Initialisation

**Goal:** Create `ExampleOutput.xlsx` with one named sheet per unique major ID found in
`toHop_THTP.xlsx`. Copy the header row from `Book1.xlsx` into each sheet.

```mermaid
flowchart TD
    A([Start Phase 1]) --> B[Read header row from Book1.xlsx]
    B --> C[Create new ExampleOutput.xlsx]
    C --> D[Iterate rows in toHop_THTP.xlsx from row 2]
    D --> E{sheet_name already\nin output workbook?}
    E -- Yes --> D
    E -- No --> F[Add sheet_name to list_id_major]
    F --> G[Create new sheet in output workbook]
    G --> H[Write Book1 header row into new sheet row 1]
    H --> D
    D --> I[All rows processed]
    I --> J[Remove default 'Sheet' tab]
    J --> K[Save ExampleOutput.xlsx]
    K --> Z([End Phase 1])
```

---

## 4. Phase 2 — Student Distribution

**Goal:** Copy each eligible application row from `Book1.xlsx` into the correct major
sheet in `ExampleOutput.xlsx`. Only rows where `Mã PTXT == '100'` are included.

```mermaid
flowchart TD
    A([Start Phase 2]) --> B[Find column index of 'Mã ngành' in Book1]
    B --> C[Find column index of 'Mã PTXT' in Book1]
    C --> D[Iterate every data row in Book1 from row 2]
    D --> E{Mã PTXT == '100'?}
    E -- No --> D
    E -- Yes --> F[Read all non-empty cell values into row_data list]
    F --> G{sheet_name exists\nin output workbook?}
    G -- No --> H[Print warning, skip row]
    H --> D
    G -- Yes --> I[Switch to major sheet]
    I --> J[Increment sheet row index counter]
    J --> K[Write row_data into next available row]
    K --> D
    D --> L[All rows processed]
    L --> M[Save ExampleOutput.xlsx]
    M --> Z([End Phase 2])
```

---

## 5. Phase 3 — Subject Combination (Khoi) Loading

**Goal:** For every major in `list_id_major`, read `toHop_THTP.xlsx` and build a
`ClassMajor` object containing all associated `ClassKhoi` objects with their subjects,
weighting coefficients (`he_so`), and gap bonus.

```mermaid
flowchart TD
    A([Start Phase 3]) --> B[For each major_id in list_id_major]
    B --> C[Create ClassMajor for major_id]
    C --> D[Iterate all rows in toHop_THTP from row 2]
    D --> E{row maNganh\n== major_id?}
    E -- No --> D
    E -- Yes --> F[Create ClassKhoi with maTohop name]
    F --> G[Set list_subject = mon1, mon2, mon3]
    G --> H[Set he_so = heSoM1, heSoM2, heSoM3]
    H --> I[Set gap_point from gap_point column]
    I --> J[Call major.add_khoi — ignores duplicates]
    J --> K{toHopGoc == 'x'\nor 'X'?}
    K -- Yes --> L[Set this khoi as primary_khoi]
    K -- No --> D
    L --> D
    D --> M[All toHop_THTP rows scanned]
    M --> N[Append ClassMajor to list_major]
    N --> B
    B --> O([End Phase 3])
```

### `add_khoi` deduplication algorithm

```mermaid
flowchart LR
    S([add_khoi called]) --> A{maToHop empty?}
    A -- Yes --> B[Append khoi directly]
    B --> Z([Return])
    A -- No --> C[Iterate existing khoi in maToHop]
    C --> D{existing.name\n== khoi.name?}
    D -- Yes --> E[Print 'already exists', return early]
    E --> Z
    D -- No --> C
    C --> F[No duplicate found — append khoi]
    F --> Z
```

---

## 6. Phase 4 — Score Calculation

### 6a. Build Book2 Lookup

**Goal:** Pre-index Book2 rows by CMND so every student lookup is O(1) instead of O(N).

```mermaid
flowchart TD
    A([build_score_lookup called]) --> B[Create empty dict lookup]
    B --> C[Iterate Book2 rows from row 2\nvalues_only=True]
    C --> D{cmnd value\nis None?}
    D -- Yes --> C
    D -- No --> E[lookup cmnd = row_values tuple]
    E --> C
    C --> F[All rows scanned]
    F --> G([Return lookup dict])
```

### 6b. Weighted Score Formula

For each subject combination (khoi), the admission score is:

$$\text{point} = 3 \times \frac{\sum_{i=1}^{3} \text{score}_i \times \text{heSo}_i}{\sum_{i=1}^{3} \text{heSo}_i}$$

Maximum possible score = **30** (all subjects score 10 with equal weights).

The **best khoi** across all combinations is selected:

$$\text{max\_point} = \max_{\text{khoi} \in \text{maToHop}} \text{point}_{\text{khoi}}$$

$$\text{max\_point\_add\_gap} = \text{max\_point} + \text{gap\_point}_{\text{best khoi}}$$

```mermaid
flowchart TD
    A([calculate_point called]) --> B[max_point = 0, best_khoi = '']
    B --> C{More khoi\nin maToHop?}
    C -- No --> Z([Return best_khoi, max_point, max_point_add_gap])
    C -- Yes --> D[sum_heso = Σ he_so for all subjects in khoi]
    D --> E{sum_heso == 0?}
    E -- Yes --> C
    E -- No --> F[weighted_sum = Σ score × he_so for each subject]
    F --> G[point = 3 × weighted_sum / sum_heso]
    G --> H{point > max_point?}
    H -- No --> C
    H -- Yes --> I[max_point = point]
    I --> J[max_point_add_gap = max_point + khoi.gap_point]
    J --> K[best_khoi = khoi.name]
    K --> C
```

### 6c. Priority Bonus Formula

The **priority-adjusted final score** applies a bonus that scales with available
headroom from the maximum score (30):

$$\text{final\_point} = \text{max\_point} + \frac{30 - \text{max\_point}}{7.5} \times \text{ut\_point}$$

Where `ut_point = KVƯT_bonus + ĐTƯT_bonus`:

| KVƯT code | Bonus |
|---|---|
| KV1 | 0.75 |
| KV2-NT / 2NT | 0.50 |
| KV2 | 0.25 |
| KV3 | 0.00 |

| ĐTƯT code | Bonus |
|---|---|
| 01–04 | 2.00 |
| 05–07 | 1.00 |
| Other | 0.00 |

```mermaid
flowchart TD
    A([calculate_ut_point called]) --> B[Get KVƯT value from row_values col 7]
    B --> C{Match KVƯT code?}
    C -- KV1 --> D[kvut = 0.75]
    C -- KV2-NT / 2NT --> E[kvut = 0.50]
    C -- KV2 --> F[kvut = 0.25]
    C -- KV3 or unknown --> G[kvut = 0.00]
    D & E & F & G --> H[Get ĐTƯT value from row_values col 6]
    H --> I{Match ĐTƯT code?}
    I -- 01-04 --> J[dtut = 2.00]
    I -- 05-07 --> K[dtut = 1.00]
    I -- other --> L[dtut = 0.00]
    J & K & L --> M([Return kvut + dtut])
```

### 6d. Per-Student Score Pipeline

```mermaid
flowchart TD
    A([Start Phase 4]) --> A1[Build book2_lookup dict once]
    A1 --> B[For each major in list_major]
    B --> C[Switch output sheet to major_id]
    C --> D[Write 3 column headers once at row 1]
    D --> E[For each student row from row 2]
    E --> F[Read CMND from row]
    F --> G{CMND found\nin book2_lookup?}
    G -- No --> E
    G -- Yes --> H[Fetch row2_values tuple]
    H --> I[calculate_point row2_values, major]
    I --> J[calculate_ut_point row2_values]
    J --> K[final_point = max_point + 30-max_point / 7.5 × ut_point]
    K --> L[final_point_gap = max_point_add_gap + same formula]
    L --> M[Write best_khoi, final_point, final_point_gap to output row]
    M --> E
    E --> N[All students processed for major]
    N --> O[Sort sheet descending by COL_DIEM_ADD_GAP]
    O --> P[Save ExampleOutput.xlsx]
    P --> B
    B --> Q([End Phase 4])
```

---

## 7. Phase 5 — Deduplication

**Goal:** A student may appear in multiple major sheets (applied to several majors).
Each student must be retained in at most one major sheet — the one they prefer
(lower NV value = higher preference). Processing stops once `TARGETS` sheets are handled.

```mermaid
flowchart TD
    A([Start Phase 5]) --> B[sheet_checked = empty list, temp_target = 0]
    B --> C[For each_sheet in list_id_major]
    C --> D[Add each_sheet to sheet_checked]
    D --> E[Switch to each_sheet]
    E --> F[For each student row in each_sheet]
    F --> G[Read current_student_id and current_student_NV from row]
    G --> H[For each_other_sheet not yet in sheet_checked]
    H --> I[Switch to each_other_sheet]
    I --> J[For each row in each_other_sheet]
    J --> K{student_id matches\nrow in other sheet?}
    K -- No --> J
    K -- Yes --> L{current NV < other NV\nAND other row index < TARGETS?}
    L -- Yes: prefer other sheet --> M[Remove row from each_sheet]
    M --> N[temp_target -= 1]
    N --> H
    L -- No: prefer this sheet --> O[Remove row from each_other_sheet]
    O --> H
    J --> H
    H --> F
    F --> P[temp_target += 1]
    P --> Q{temp_target\n== TARGETS?}
    Q -- Yes --> R[Save and stop early]
    Q -- No --> C
    C --> R[Save ExampleOutput.xlsx]
    R --> Z([End Phase 5])
```

---

## 8. Full End-to-End Sequence

```mermaid
sequenceDiagram
    participant M  as main.py
    participant EH as ExcelHandler
    participant CF as common_func
    participant FS as File System

    M->>FS: Read toHop_THTP.xlsx, Book1.xlsx, Book2.xlsx
    FS-->>M: Workbook objects

    rect rgb(230,240,255)
        note over M,EH: Phase 1 — Initialise output workbook
        M->>FS: Create ExampleOutput.xlsx (blank)
        M->>EH: load ExampleOutput.xlsx
        loop For each unique maNganh in toHop_THTP
            M->>EH: add_sheet(major_id)
            M->>EH: write Book1 header row into sheet
        end
        M->>EH: remove_sheet("Sheet")
        M->>FS: save ExampleOutput.xlsx
    end

    rect rgb(230,255,230)
        note over M,EH: Phase 2 — Distribute applicants
        loop For each Book1 row where PTXT == '100'
            M->>EH: chosse_current_sheet(major_id)
            M->>EH: write student row into next available row
        end
        M->>FS: save ExampleOutput.xlsx
    end

    rect rgb(255,245,220)
        note over M,EH: Phase 3 — Load subject combinations
        loop For each major_id
            loop For each matching row in toHop_THTP
                M->>M: create ClassKhoi with subjects + he_so + gap
                M->>M: ClassMajor.add_khoi(khoi)
            end
        end
    end

    rect rgb(255,230,230)
        note over M,CF: Phase 4 — Calculate scores
        M->>CF: build_score_lookup(Book2, cmnd_col)
        CF-->>M: dict{cmnd → row_values}
        loop For each major
            M->>EH: write 3 result headers once
            loop For each student row
                M->>CF: calculate_point(row_values, major)
                CF-->>M: best_khoi, max_point, max_point_add_gap
                M->>CF: calculate_ut_point(row_values)
                CF-->>M: ut_point
                M->>M: apply priority bonus formula
                M->>EH: write scores to output row
            end
            M->>EH: sort_inc_base_on_column_index(COL_DIEM_ADD_GAP)
            M->>FS: save ExampleOutput.xlsx
        end
    end

    rect rgb(240,230,255)
        note over M,EH: Phase 5 — Deduplication
        loop For each sheet (until TARGETS reached)
            loop For each student in sheet
                loop For each not-yet-checked other sheet
                    alt Student found in other sheet
                        M->>EH: remove lower-preference duplicate row
                    end
                end
            end
        end
        M->>FS: save ExampleOutput.xlsx
    end
```

---

## 9. Full End-to-End Activity Diagram

```mermaid
flowchart TD
    START([Program Start]) --> LOAD[Load 3 input workbooks]
    LOAD --> PH1

    subgraph PH1[Phase 1 · Initialise Output]
        P1A[Read Book1 header row] --> P1B[Scan toHop_THTP for unique major IDs]
        P1B --> P1C[Create one output sheet per major with header]
        P1C --> P1D[Remove default blank sheet]
        P1D --> P1E[Save output file]
    end

    PH1 --> PH2

    subgraph PH2[Phase 2 · Distribute Applicants]
        P2A[Find Mã ngành and Mã PTXT columns] --> P2B[Filter rows: PTXT == '100']
        P2B --> P2C[Append row to matching major sheet]
        P2C --> P2D[Save output file]
    end

    PH2 --> PH3

    subgraph PH3[Phase 3 · Build Major Objects]
        P3A[For each major_id] --> P3B[Scan toHop_THTP for matching rows]
        P3B --> P3C[Build ClassKhoi with subjects + weights + gap]
        P3C --> P3D[Add to ClassMajor — deduplicate by name]
        P3D --> P3E[Mark primary khoi if toHopGoc == 'x']
    end

    PH3 --> PH4

    subgraph PH4[Phase 4 · Score Calculation]
        P4A[Build CMND→row lookup dict from Book2] --> P4B[For each major]
        P4B --> P4C[Write result column headers]
        P4C --> P4D[For each student row]
        P4D --> P4E{CMND in lookup?}
        P4E -- No, skip --> P4D
        P4E -- Yes --> P4F[calculate_point → best khoi + max score]
        P4F --> P4G[calculate_ut_point → priority bonus]
        P4G --> P4H[Apply priority bonus formula]
        P4H --> P4I[Write scores to output row]
        P4I --> P4D
        P4D --> P4J[Sort sheet by final_point_add_gap descending]
        P4J --> P4K[Save output file]
        P4K --> P4B
    end

    PH4 --> PH5

    subgraph PH5[Phase 5 · Deduplication]
        P5A[For each sheet in order] --> P5B[For each student in sheet]
        P5B --> P5C[Search for same student in other sheets]
        P5C --> P5D{Found in\nanother sheet?}
        P5D -- No --> P5B
        P5D -- Yes --> P5E{Current sheet\nmore preferred?}
        P5E -- Yes: keep here --> P5F[Remove from other sheet]
        P5E -- No: prefer other --> P5G[Remove from current sheet]
        P5F & P5G --> P5B
        P5B --> P5H{Processed TARGETS\nsheets?}
        P5H -- Yes --> P5I[Save and exit early]
        P5H -- No --> P5A
        P5A --> P5I[Save output file]
    end

    PH5 --> END([Program End · Print elapsed time])
```

---

## 10. Subject Column Mapping Reference

These are 0-based column indices in `Book2.xlsx` (Sheet1).
When `FIXED_FORMAT = True` these values are used directly.
When `FIXED_FORMAT = False` they are discovered by scanning the header row.

| Subject Code | Meaning | 0-based Column |
|---|---|---|
| `TO` | Toán (Math) | 26 |
| `VA` | Văn (Literature) | 27 |
| `LI` | Lý (Physics) | 28 |
| `HO` | Hoá (Chemistry) | 29 |
| `SI` | Sinh (Biology) | 30 |
| `SU` | Sử (History) | 31 |
| `DI` | Địa (Geography) | 32 |
| `GDCD` | Giáo dục công dân (Civic Education) | 33 |
| `NN` | Ngoại ngữ (Foreign Language) | 34 |
| `KVƯT` | Khu vực ưu tiên (Priority Region) | 7 |
| `ĐTƯT` | Đối tượng ưu tiên (Priority Category) | 6 |

---

## 11. Priority Bonus Tables

### KVƯT — Priority Region (Khu vực ưu tiên)

| Cell Value | Bonus Points |
|---|---|
| `KV1` | 0.75 |
| `KV2-NT` or `2NT` | 0.50 |
| `KV2` | 0.25 |
| `KV3` | 0.00 |
| Anything else | 0.00 |

### ĐTƯT — Priority Category (Đối tượng ưu tiên)

| Cell Value | Bonus Points |
|---|---|
| `01`, `02`, `03`, `04` | 2.00 |
| `05`, `06`, `07` | 1.00 |
| Anything else | 0.00 |

### Combined Priority Bonus

$$\text{ut\_point} = \text{KVƯT\_bonus} + \text{ĐTƯT\_bonus}$$

Maximum possible `ut_point` = **2.75** (KV1 = 0.75 + group-1 category = 2.00).

### Final Score with Priority

$$\text{final\_point} = \text{max\_point} + \frac{30 - \text{max\_point}}{7.5} \times \text{ut\_point}$$

$$\text{final\_point\_add\_gap} = \text{max\_point\_add\_gap} + \frac{30 - \text{max\_point\_add\_gap}}{7.5} \times \text{ut\_point}$$

The factor $\frac{30 - \text{max\_point}}{7.5}$ ensures that students with higher base
scores gain proportionally less from priority bonuses, capping the total score at 30.
