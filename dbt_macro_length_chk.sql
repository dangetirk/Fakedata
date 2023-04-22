{% test test_length(model, column_name, max_length) %}
SELECT
  1
FROM
  {{ model }}
WHERE
  LENGTH({{ column_name }}) > {{ max_length }}
{% endtest %}
