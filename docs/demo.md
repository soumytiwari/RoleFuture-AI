# RoleFuture AI — Demo Checklist

## 1. Open the dashboard

Show the role count, activity count, ranking, and impact metrics.

## 2. Search an existing role

Use the search box. Select a saved role from the alphabetically sorted matches.

## 3. Explain one role

Open a role such as Finance Analyst and show:

- Processes
- Activities
- Current skills
- Future skills
- Future responsibilities
- Exposure / automation / augmentation scores
- The 1–5 assessment factors
- The assessment rationale

Explain that Python calculates the numerical results.

## 4. Show AI analysis

Click **Generate AI analysis**. The page identifies whether the result came from the local model or the deterministic fallback.

Explain:

> The model explains the structured analysis. It does not decide the scores.

## 5. Compare two roles

Open the Compare page and select two roles.

Show the numeric differences first, then the AI/fallback comparison explanation.

## 6. Create a new role

From the dashboard search box, enter a role not already saved.

Add a short description if useful. Click **Create and analyse this role**.

Show that the application creates processes, activities, assessment factors, scores, skills, and future responsibilities and then saves the new role.

## 7. Demonstrate fallback

Start the application with an unreachable Ollama URL:

```bash
OLLAMA_BASE_URL=http://127.0.0.1:11499 uvicorn app.main:app --reload
```

Open the same role again. The page should still work and label the result as the deterministic fallback.

## 8. Finish with the API

Open `/docs` and briefly show the role, comparison, ranking, AI, and role-creation endpoints.

## Re-analysing an existing role

A saved role can be re-analysed from its role-detail page. The user can update the department or description and select **Re-analyse and save**. The application keeps the same role ID and replaces the generated processes, activities, assessment factors, scores, skills, responsibilities, and future profile. It does not create a duplicate role.

The regenerated profile uses the local Ollama model when available. When Ollama is unavailable, the deterministic fallback generator creates the replacement profile and the same Python scoring engine calculates the numerical results.
