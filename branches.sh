#!/usr/bin/env bash
#
#
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

# here comes execution (we base on )
changes=$(git status models --porcelain)
if [[ -z "$changes" ]]; then
    echo "No changes in models, nothing to commit - stopping execution"
    exit 0
fi

echo "models changed, preparing commit"
git add models/
git commit -m "PEA views automation: \n\nChanges:\n$changes"


