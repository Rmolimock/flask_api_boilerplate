from pytest_bdd import scenario, given, when, then
from pytest_bdd.parsers import cfparse as parse
from tests.step_defs import CONVERTERS


@scenario('../features/run_as_is.feature', 'Objects can be saved to and loaded from the database')
def test_save_and_load_with_db():
    pass


@given(parse('an object is created in memory'), target_fixture='object')
def object_created():
    try:
        from models.boilerplate_model import BoilerplateModel
        data = {
            'boiler': 'test_name',
            'plate': 'test_data'
        }
        object_instance = BoilerplateModel(data)
        assert object_instance
        return object_instance
    except Exception as e:
        print('--', e)
        raise e


@given(parse('it has data that must persist'))
def has_data_that_must_persist(object):
    try:
        assert object.persistent_data()
    except Exception as e:
        print('--', e)
        assert False

@when(parse('it is saved'))
def is_saved(object):
    try:
        object.save()
        pass
    except Exception as e:
        print('--', e)
        assert False

@when(parse('it is loaded by id'), target_fixture='loaded_object')
def is_loaded_by_id(object):
    try:
        from models.boilerplate_model import BoilerplateModel
        loaded_object = BoilerplateModel.load_from_id(object.id)
        assert loaded_object
        return loaded_object
    except Exception as e:
        print('--', e)
        assert False

@then(parse('the loaded data matches the saved data'))
def data_matches(object, loaded_object):
    assert object.persistent_data() == loaded_object.persistent_data()




'''

  And it is loaded by id
  Then the loaded data matches the saved data
  '''