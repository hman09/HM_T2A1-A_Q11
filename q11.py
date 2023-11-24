from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['DATABASE_USE'] = # Database connection string.

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Sample(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String(100))
    bool = db.Column(db.Boolean, default=False)

class SampleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'string', 'bool')


@app.route('/sample/create', methods=['POST'])
def create():
    sample_data = SampleSchema().load(request.json)
    sample = Sample(
        string=sample_data['string'],
        bool=True
    )

    db.session.add(sample)
    db.session.commit()

    return SampleSchema()

@app.route('/sample/remove', methods=['POST'])
def create():
    sample_data = SampleSchema().load(request.json)
    sample = Sample(
        string=sample_data['string'],
        bool=True
    )

    db.session.delete(sample)
    db.session.commit()

    return SampleSchema()

@app.route('/sample/update', methods=['POST'])
def update():
    sample_data = SampleSchema().load(request.json)
    samples_to_update = Sample.query.filter_by(bool=False, string='your_specific_value').all()

    for sample in samples_to_update:
        sample.string = sample_data['string']
        sample.bool = True

    db.session.commit()

    return SampleSchema(many=True)


@app.route('/sample/retieve')
def all_samples():
    samples = Sample.query.filter(Sample.bool != 'Done').all()
    return SampleSchema(many=True).dump(samples)

