import pytest

from protean.core.projection import BaseProjection
from protean.exceptions import InvalidDataError, NotSupportedError
from protean.fields import Integer, String
from protean.utils.container import BaseContainer, OptionsMixin
from protean.utils.reflection import declared_fields


class CustomContainerMeta(BaseContainer):
    def __new__(cls, *args, **kwargs):
        if cls is CustomContainerMeta:
            raise TypeError("CustomContainerMeta cannot be instantiated")
        return super().__new__(cls)


class CustomContainer(CustomContainerMeta, OptionsMixin):
    foo = String()
    bar = String()


def test_that_base_container_class_cannot_be_instantiated():
    with pytest.raises(NotSupportedError) as exc:
        BaseContainer()

    assert str(exc.value) == "BaseContainer cannot be instantiated"


class TestContainerInitialization:
    def test_that_base_container_class_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            CustomContainerMeta()

    def test_abstract_containers_cannot_be_instantiated(self, test_domain):
        class AbstractProjection(BaseProjection):
            foo = String()

        test_domain.register(AbstractProjection, abstract=True)

        with pytest.raises(NotSupportedError) as exc:
            AbstractProjection(foo="bar")

        assert (
            str(exc.value)
            == "AbstractProjection class has been marked abstract and cannot be instantiated"
        )

    def test_that_a_concrete_custom_container_can_be_instantiated(self):
        custom = CustomContainer(foo="a", bar="b")
        assert custom is not None

    def test_that_init_args_object_needs_to_be_a_dict(self):
        with pytest.raises(AssertionError) as exc:
            CustomContainer("a", "b")

        assert str(exc.value) == (
            "Positional argument 'a' passed must be a dict. "
            "This argument serves as a template for loading common values."
        )


class TestContainerProperties:
    def test_two_containers_with_equal_values_are_considered_equal(self):
        custom1 = CustomContainer(foo="a", bar="b")
        custom2 = CustomContainer(foo="a", bar="b")

        assert custom1 == custom2

    def test_output_to_dict(self):
        custom = CustomContainer(foo="a", bar="b")
        assert custom.to_dict() == {"foo": "a", "bar": "b"}

    def test_that_only_valid_attributes_can_be_assigned(self):
        custom = CustomContainer(foo="a", bar="b")
        with pytest.raises(InvalidDataError) as exc:
            custom.baz = "c"

        assert exc.value.messages == {"baz": ["is invalid"]}


class TestContainerInheritance:
    def test_field_order_after_inheritance(self):
        class ChildCustomContainer(CustomContainer):
            baz = String()

        assert list(declared_fields(ChildCustomContainer).keys()) == [
            "foo",
            "bar",
            "baz",
        ]

    def test_field_order_when_overridden_after_inheritance(self):
        class ChildCustomContainer(CustomContainer):
            baz = String()
            foo = Integer()

        assert list(declared_fields(ChildCustomContainer).keys()) == [
            "foo",
            "bar",
            "baz",
        ]
        assert isinstance(declared_fields(ChildCustomContainer)["foo"], Integer)
