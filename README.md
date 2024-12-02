# AWS Taggable
Search AWS Tagging API for all services

## jq
Get Tagging Actions
```bash
jq -r 'to_entries[] | .key as $service | $service + ":" + .value.actions[] | select(. | contains("Tag"))' aws_actions.json > tag_actions.txt@[gist]
```
Get Taggable Services
```bash
jq -r 'to_entries[] | select(.value.actions | any(contains("Tag"))) | .key' aws_actions.json > taggable_service.txt
```

## Scrap
https://zenn.dev/nag0yan/scraps/9e14c28fbcace9
