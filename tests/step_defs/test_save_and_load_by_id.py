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
        print('--', e)
        print('\nobject_instance:', object_instance)
        raise e


@given(parse('it has data that must persist'), target_fixture='saved_object_data')
def has_data_that_must_persist(object):
    try:
        saved_object_data = object.persistent_data()
        assert saved_object_data
        return saved_object_data
    except Exception as e:
        print('--', e)
        print('\nsaved_object_data:', saved_object_data)
        assert False

@when(parse('it is saved'))
def is_saved(object):
    try:
        object.save()
        pass
    except Exception as e:
        print('--', e)
        print('\nobject:', object)
        assert False

@when(parse('it is loaded by id'), target_fixture='loaded_by_id_object')
def is_loaded_by_id(saved_object_data):
    try:
        from models.boilerplate_model import BoilerplateModel
        id = saved_object_data.get('id')
        loaded_by_id_object = BoilerplateModel.load_by_id(id)
        assert loaded_by_id_object
        return loaded_by_id_object
    except Exception as e:
        print('--', e)
        loaded_by_id_object.delete()
        print('\nid:', saved_object_data.get('id'))
        print('\nloaded_object:', loaded_by_id_object)
        assert False

@when(parse('it is loaded by an arbitrary attribute'), target_fixture='loaded_by_attr_object')
def is_loaded_by_attribute(saved_object_data):
    try:
        from models.boilerplate_model import BoilerplateModel
        attribute = 'boiler'
        value = saved_object_data.get(attribute)
        loaded_by_attr_object = BoilerplateModel.query.filter_by(boiler=value).first()
        assert loaded_by_attr_object
        return loaded_by_attr_object
    except Exception as e:
        print('--', e)
        print('\nattribute:', attribute)
        print('\nvalue:', saved_object_data.get(attribute))
        print('\nloaded_object:', loaded_by_attr_object)
        loaded_by_attr_object.delete()
        assert False

@then(parse('the data loaded by id matches the saved data'))
def data_by_id_matches(saved_object_data, loaded_by_id_object):
    try:
        assert saved_object_data == loaded_by_id_object.persistent_data()
        loaded_by_id_object.delete()
    except AssertionError as e:
        print('--', e)
        loaded_by_id_object.delete()
        print('\nsaved_object_data:', saved_object_data)
        print('\nloaded_object_data:', loaded_by_id_object.persistent_data())
        assert False

@then(parse('the data loaded by an arbitrary attribute matches the saved data'))
def data_by_attr_matches(saved_object_data, loaded_by_attr_object):
    try:
        assert saved_object_data == loaded_by_attr_object.persistent_data()
    except AssertionError as e:
        print('--', e)
        print('\nsaved_object_data:', saved_object_data)
        print('\nloaded_object_data:', loaded_by_attr_object.persistent_data())
        assert False


'''
  Then the data loaded by id matches the saved data
  Then the data loaded by an arbitrary attribute matches the saved data
'''