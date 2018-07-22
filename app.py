import tempfile

from flask import Flask, request, jsonify, send_file
import pypandoc


app = Flask(__name__)

@app.route("/convert/json", methods=['POST'])
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

    filters = data.get('filters', [])
    extra_args = data.get('extra_args', [])

    with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
        pypandoc.convert_text(body, to,
                              format=from_,
                              outputfile=f.name,
                              filters=filters,
                              extra_args=extra_args)
        return send_file(f.name)


if __name__ == '__main__':
    app.run(debug=True)
