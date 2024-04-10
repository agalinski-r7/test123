## Description
<!-- Describe what this change does and why it is needed. -->
<!-- Add JIRA link if applicable -->


## Checklist (Mark "X" or "N/A" in each [] for each PR)

### Common
- [ ] I confirm that the branch name contains relevant Jira ticket number.
- [ ] I acknowledge that I will comment in my Jira ticket the details of the feature (i.e. table or field name, link to documentation) + get signoff from requestor (either in the ticket or I will add comment myself if done outside of ticket).
- [ ] I have followed Staging to PROD [process](https://localhost) (PII, data category checks, etc.)?
- [ ] I have followed our unit test [standards](https://localhost))
- [ ] I have run updated transform in QA/Dev, and validated test results (provide details in Testing section below).
- [ ] I have updated documentation (e.g. [Lakehouse Production Datasets](https://localhost)), including data dictionaries (if applicable).

### Details
- [ ] This change require us to notify stakeholders:
  - [ ] I have prepared a note to send to #snowflake-developers and other relevant channels
- [ ] This is a temporary change:
  - [ ] I have placed appropriate comment(s) in the code.
  - [ ] I have written down clear criteria of finishing the work with the change in a ticket (either current or new).
- [ ] I'm adding new schema:
  - [ ] I have added future grants for all roles that require access to future tables and views within the new schema.
  - [ ] I acknowledge that in case of `SAILPOINT_VALIDATION` test failure I might need to verify if my schema is covered by the procedure and possibly add an exception, as explained in the wiki: []().
- [ ] I'm adding a new table/view:
  - [ ] I have followed [the procedure for testing net new dataset](https://localhost)?
  - [ ] I have updated the [data tagging stored procedure](https://localhost).
  - [ ] This is a P1 object:
    - [ ] I have updated the P1 Pipelines [spreadsheet](https://localhost).
- [ ] I'm deprecating an object:
  - [ ] I have checked if object is actually unused
  - [ ] I have moved the object definition to a respective `deprecated` folder
  - [ ] I have added note about deprecation to the wiki
  - [ ] I have notified about deprecation on #snoflake-developers

### Completion
  - [ ] I went through the checklist, marking all relevant items.

## Testing
<!-- Describe how this change was tested. -->

<!-- For more information see: https://localhost

