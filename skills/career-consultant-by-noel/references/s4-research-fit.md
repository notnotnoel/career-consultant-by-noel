# S4 · Research and fit

Goal: understand the role well enough to decide whether to apply, and to give S5 one clear priority order. You arrive here from a shared JD (skipping S2–S3) or from a role picked in the tracker.

## Steps

1. **Folder and tracker.** Run:

   ```bash
   python scripts/workspace.py new-job "<folder>" --company "<Company>" --role "<Role>" --link "<url>" --step Researching
   ```

   Save the JD into the new `00_JD/` as text or PDF. If you only have a link, fetch the posting and save its text. Postings disappear, and later states need the exact wording.

2. **Classify the JD.**
   - Function and seniority.
   - The real mandate: what the person will actually be judged on, which is often not the first bullet.
   - Must-haves vs nice-to-haves.

3. **Research the company.** Look at the last 3–6 months:
   - results
   - strategy shifts
   - M&A
   - leadership changes
   - hiring or layoff signals

   Cite sources. This is what makes S5's profile line and S7's opening sentence specific to them.

4. **Research the people.** Find the likely hiring manager and reporting line from public professional sources: LinkedIn, the company site, press. Mark guesses as guesses, and keep to professional information.

5. **Set the priority criterion.** Write one explicit order, for example *pricing analytics > stakeholder influence > SQL depth*, with a one-line reason. It's the spine of S5. It decides what gets full bullets and what gets compressed.

6. **Build the fit table.**

   | Requirement | Evidence from the twin | Verdict |
   |---|---|---|
   | 5+ yrs pricing or revenue management | Fabrikam pricing lead 2021–24, Contoso analyst 2019–21 | ✅ |
   | Tableau | Power BI dashboards for 3 regions | 🟡 |
   | Mandarin | — | 🔴 |

   - Fill gaps only from the twin.
   - Ask about any 🔴 that might exist but isn't recorded ("The JD wants Tableau. Have you used it?").
   - Write any new answers into the twin, following S1.

7. **Give a verdict.** Choose one of:
   - Apply
   - Apply with caveats
   - Skip

   Give the reason in at most three lines, plus the fit score: Fit = 100 × (2 × must-have credit + nice-to-have credit) ÷ (2 × number of must-haves + number of nice-to-haves), with ✅ = 1, 🟡 = 0.5, 🔴 = 0, capped at 45 if a hard-gate must-have is 🔴.

8. **Suggest a new chat.** Recommend starting a new chat in the Project for this application, named `<Company> · <Role> · S5`, then continue to S5 if the user wants the CV now.
