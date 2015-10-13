#/bin/bash
set -x

start_time=$(date +"%s")

# Abdallah environment variable
export JOB_ID={{ job.id }}
export JOB_URL={{ job.full_url }}

curl -X PATCH -d '{"status": "INI"}' -H "Content-Type: application/json" $JOB_URL
# Environmental variable
{% for var in env %}
export {{ var|safe }}
{% endfor %}

# Clone repository
git clone --depth=50 {{ repository }} /source
cd /source
git fetch origin {{ commit }}
git checkout -f FETCH_HEAD

# Install
{% for cmd in install %}
{{ cmd|safe }}
{% endfor %}

# Run tests
curl -X PATCH -d '{"status": "STA"}' -H "Content-Type: application/json" $JOB_URL
{% for cmd in script %}
{{ cmd|safe }} || (curl -X PATCH -d '{"status": "FAI"}' -H "Content-Type: application/json" $JOB_URL && exit 1)
{% endfor %}
curl -X PATCH -d '{"status": "PAS"}' -H "Content-Type: application/json" $JOB_URL

# After script
{% for cmd in after_script %}
{{ cmd|safe }}
{% endfor %}

end_time=$(date +"%s")
elapsed_time=$((end_time - start_time))
curl -X PATCH -d "{\"elapsed_time\": ${elapsed_time}}" -H "Content-Type: application/json" $JOB_URL
exit 0
