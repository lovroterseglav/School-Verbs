from flask import Flask, render_template, request

from web.structure import EnglishVerbAnswer, EnglishVerb

app = Flask("nemscina")


@app.route('/')
def index():
    verb_name = "biti"
    return render_template("ang_input_form.html", verb=verb_name, render_submit=True)


@app.route('/submit_ang/<verb_name>', methods=['POST'])
def submit(verb_name):
    verb = EnglishVerbAnswer(request.form.get('infinitive'), request.form.get('past'), request.form.get('past_participle'))
    verb_solution = EnglishVerb("be", "was", "were", verb_name)
    return render_template('ang_input_form.html', render_submit=False, verb=verb_name, infinitive=verb.infinitive, past=verb.past, past_participle=verb.past_participle,
                           infinitive_correct=verb_solution.infinitive, past_correct=verb_solution.past, past_participle_correct=verb_solution.past_participle)


if __name__ == '__main__':
    app.run(debug=True)
