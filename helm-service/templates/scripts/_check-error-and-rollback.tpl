{{- define "check-error-and-rollback.py" -}}
{{ .Files.Get "scripts/check-error-and-rollback.py" | indent 4 }}
{{- end }}