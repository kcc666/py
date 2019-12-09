from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/search')
def search():
    # arguments
    condition = request.args.get('q')

    return '用户提交的查询参数是: {}'.format(condition)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8081)
    print("www")
