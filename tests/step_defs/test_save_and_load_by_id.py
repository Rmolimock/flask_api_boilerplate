from pytest_bdd import scenario, given, when, then
from pytest_bdd.parsers import cfparse as parse
from tests.step_defs import CONVERTERS


@scenario('../features/run_as_is.feature', 'Objects can be saved to and loaded from the database by their id')
def test_save_and_load_with_db():
    pass


@given(parse('an object is created in memory'), target_fixture='object')
def object_created():
    try:
        from models.boilerplate_model import BoilerplateModel
        from uuid import uuid4
        data = {
            'name': str(uuid4()),
            'boiler': 'test_boiler',
            'plate': 'test_plate'
        }
        object_instance = BoilerplateModel(**data)
        assert object_instance
        return object_instance
    except Exception as e:
        print('object_instance:', object_instance)
        print('--', e)
        raise e


@given(parse('it has data that must persist'), target_fixture='saved_object_data')
def has_data_that_must_persist(object):
    try:
        saved_object_data = object.persistent_data()
        assert saved_object_data
        return saved_object_data
    except Exception as e:
        print('saved_object_data:', saved_object_data)
        print('--', e)
        assert False

@when(parse('it is saved'))
def is_saved(object):
    try:
        object.save()
        pass
    except Exception as e:
        print('object:', object)
        print('--', e)
        assert False

@when(parse('it is loaded by id'), target_fixture='loaded_object')
def is_loaded_by_id(saved_object_data):
    try:
        from models.boilerplate_model import BoilerplateModel
        id = saved_object_data.get('id')
        loaded_object = BoilerplateModel.load_by_id(id)
        assert loaded_object
        return loaded_object
    except Exception as e:
        loaded_object.delete()
        print('id:', saved_object_data.get('id'))
        print('loaded_object:', loaded_object)
        print('--', e)
        assert False

@then(parse('the loaded data matches the saved data'))
def data_matches(saved_object_data, loaded_object):
    try:
        assert saved_object_data == loaded_object.persistent_data()
        loaded_object.delete()
    except AssertionError as e:
        loaded_object.delete()
        print('saved_object_data:', saved_object_data)
        print('loaded_object_data:', loaded_object.persistent_data())
        print('--', e)
