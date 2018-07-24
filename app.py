import tempfile

from flask import Flask, request, jsonify, send_file
from flask_basicauth import BasicAuth
import pypandoc
import yaml


with open('config.yaml') as f:
    config = yaml.load(f)

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = config['username']
app.config['BASIC_AUTH_PASSWORD'] = config['password']

basic_auth = BasicAuth(app)

@app.route("/json", methods=['POST'])
@basic_auth.required
def convert():
    data = request.get_json()

    if data is None:
        return jsonify(error="No JSON data")

    try:
        to = data['to']
        from_ = data['from']
        body = data['body']
    except KeyError as e:
        return jsonify(error=f"JSON body must contain {e} key")

    file_name = data.get('file_name', 'document.pdf')
    filters = data.get('filters', [])
    extra_args = data.get('extra_args', [])

    with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
        pypandoc.convert_text(body, to,
                              format=from_,
                              outputfile=f.name,
                              filters=filters,
                              extra_args=extra_args)
        return send_file(f.name, 
                         as_attachment=True, 
                         attachment_filename=file_name)


if __name__ == '__main__':
    app.run(debug=True)
