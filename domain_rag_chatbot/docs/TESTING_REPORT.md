# Testing and Evaluation Report

## Test environment
- Python 3.10+
- Streamlit
- FAISS
- Sentence Transformers
- Groq API
- Sample policy and handbook PDFs

## Evaluation criteria
1. Retrieval accuracy
2. Answer correctness
3. Groundedness
4. Refusal quality
5. Source quality
6. Response time

## 15-question evaluation set
The detailed questions are stored in `tests/test_questions.csv`.

| # | Test | Expected |
|---|---|---|
| 1 | Standard leave entitlement | Relevant policy passage |
| 2 | Leave request process | Relevant policy passage |
| 3 | Attendance recording | Relevant handbook passage |
| 4 | Workday start time | Relevant handbook passage |
| 5 | Late-arrival procedure | Relevant handbook passage |
| 6 | Workplace incident reporting | Relevant policy passage |
| 7 | Departmental leave approval | Relevant policy passage |
| 8 | Record retention | Relevant policy passage |
| 9 | Visitor procedure | Relevant handbook passage |
| 10 | Remote-work request | Relevant policy passage |
| 11 | Dress requirement | Relevant handbook passage |
| 12 | Company asset handling | Relevant policy passage |
| 13 | Confidential information | Relevant policy passage |
| 14 | Cafeteria opening time | Relevant handbook passage |
| 15 | Current company CEO | Refusal because unavailable |

## Execution procedure
For each question:
1. Upload and process the sample PDFs.
2. Ask the question.
3. Record the displayed source document and page.
4. Check whether the answer is supported by the displayed context.
5. Mark Correct/Incorrect.
6. For test 15, verify that the required fallback is returned.

## Suggested evaluation table

| Question | Expected Source | Retrieved Source | Correct? | Grounded? | Notes |
|---|---|---|---|---|---|
| 1 | company_policy.pdf | | | | |
| 2 | company_policy.pdf | | | | |
| 3 | employee_handbook.pdf | | | | |
| ... | ... | | | | |
| 15 | Not available | | | | |

## Component tests
Run:

```bash
pytest -q
```

The included tests verify sample PDF availability, PDF extraction metadata and chunking behavior.
