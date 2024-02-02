#!/usr/bin/env bash
#

pea_view_branches=$(git branch --list 'pea_view_automation*' | sed 's/^[* ] //' | sort -r )
matching_branch_count=$(echo "$pea_view_branches" | grep -c .)


if [[ "$matching_branch_count" -eq 0 ]]; then
    branch_type='new'
    target_branch_name=pea_view_automation_$(date '+%Y%m%d')
    echo "No matches, creating new branch: $target_branch_name"
    git branch "$target_branch_name"
elif [[ "$matching_branch_count" -eq 1 ]]; then
    branch_type='existing'
    target_branch_name=$pea_view_branches
    echo "Single match, reusing $target_branch_name"
else
    branch_type='existing'
    target_branch_name=$(echo "$pea_view_branches" | head -1)
    echo -e "More than 1 matching branch name: \n$pea_view_branches\n\nUsing the newest one: $target_branch_name"
fi

git checkout "$target_branch_name"

###############################################################################
# 
# this is where DBT changes happen (we want to start off with the target branch
# to avoid any conflicts). In case of emergency we can always drop all branches
# and all PRs, and execute process manually.
# 
###############################################################################

touch models/foo4

changes=$(git status models --porcelain)
if [[ -z "$changes" ]]; then
    echo "No changes in models, nothing to commit - stopping execution"
    exit 0
fi

echo "Models changed, committing change"
git add models/
git commit -m "PEA views automation: \n\nChanges:\n$changes"

# ------------------
echo "Checking if we have an existing PR to reuse: $target_branch_name->master"

pr_exists=$(gh pr list --state open --head "$target_branch_name" --base master  | grep -q .)

if [[ "$pr_exists" ]]; then
    echo "PR from this branch already exists" 

    is_it_a_draft_pr=$(gh pr list --state open --head "$target_branch_name" --base master --json isDraft -q '.[] | select(.isDraft==true)' | grep -q .)
    if [[ $"is_it_a_draft_pr" ]]; then
        echo "It's a draft PR, no changes needed"
    else
        echo "It's not a draft PR, demoting it before push to avoid automatic DBT build that could spill PII data"
        pr_number=$(gh pr list --state open --head "$target_branch_name" --base master --json isDraft,number -q '.[] | select(.isDraft==true) | .number')
        gh pr edit "$pr_number" --draft
    fi

    echo "Pushing the change"
    git push -u origin HEAD

    echo "PR already open (optionally I can add a notification here)"
else
    echo "PR doesn't exist, creating a new one"

    echo "Pushing the change"
    git push -u origin HEAD

    echo "Creating a draft PR"
    gh pr create --title "Auto-PR $(date +%Y%d%d)" --body "Auto-generated update" --draft

    echo "PR open (optionally I can add a notification here)"
fi
