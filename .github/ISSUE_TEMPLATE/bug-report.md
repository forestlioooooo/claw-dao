name: Bug Report
description: Report something that isn't working as expected
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        ## Description
        Describe the bug clearly

  - type: input
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
      placeholder: 1. Go to...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      placeholder: What should happen?

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      placeholder: What actually happened?
