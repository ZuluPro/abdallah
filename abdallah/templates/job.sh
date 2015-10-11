#/bin/bash
cat /init.sh
set -e
{% if DEBUG_CONTAINER %}set -x{% endif %}
set -x

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
{% for cmd in script %}
{{ cmd|safe }}
{% endfor %}
