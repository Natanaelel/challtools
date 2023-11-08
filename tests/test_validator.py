from challtools.validator import ConfigValidator, CTFValidator


def get_min_valid_config():
    return {
        "title": "testing challenge",
        "description": "testing description",
        "authors": "testing author",
        "categories": "testing category",
        "flag_format_prefix": "pytest{",
        "flags": "test_flag",
        "spec": "0.0.1",
    }


class Test_A002:
    def test_invalid(self):
        validator = ConfigValidator({})

        success, errors = validator.validate()
        assert not success
        assert any([error["code"] == "A002" for error in errors])


class Test_A005:
    def test_valid(self):
        config = get_min_valid_config()
        config["flags"] = [{"type": "regex", "flag": "^test_flag$"}]
        validator = ConfigValidator(config)

        success, errors = validator.validate()
        assert success
        assert not any([error["code"] == "A005" for error in errors])

    def test_warn(self):
        config = get_min_valid_config()
        config["flags"] = [{"type": "regex", "flag": "test_flag"}]
        validator = ConfigValidator(config)

        success, errors = validator.validate()
        assert success
        assert any([error["code"] == "A005" for error in errors])


class Test_A006:
    def test_valid(self):
        config = get_min_valid_config()
        config["custom_service_types"] = [
            {"type": "ssh", "display": "ssh display"},
            {"type": "gopher", "display": "gopher display"},
        ]
        validator = ConfigValidator(config)

        success, errors = validator.validate()

        assert success
        assert not any([error["code"] == "A006" for error in errors])

    def test_invalid(self):
        config = get_min_valid_config()
        config["custom_service_types"] = [
            {"type": "ssh", "display": "ssh display"},
            {"type": "ssh", "display": "ssh display number two"},
        ]
        validator = ConfigValidator(config)

        success, errors = validator.validate()

        assert success
        assert any([error["code"] == "A006" for error in errors])


class Test_B005:
    def test_valid(self):
        config1 = get_min_valid_config()
        config1["challenge_id"] = "0001"

        config2 = get_min_valid_config()
        config2["challenge_id"] = "0002"
        validator = CTFValidator({}, [config1, config2], ["", ""])

        success, errors = validator.validate()

        assert success
        assert not any([error["code"] == "B005" for error in errors])

    def test_invalid(self):
        config1 = get_min_valid_config()
        config1["challenge_id"] = "0001"

        config2 = get_min_valid_config()
        config2["challenge_id"] = "0001"
        validator = CTFValidator({}, [config1, config2], ["", ""])

        success, errors = validator.validate()

        assert success
        assert any([error["code"] == "B005" for error in errors])


class Test_B006:
    def test_valid(self):
        config1 = get_min_valid_config()
        config1["title"] = "chall title"

        config2 = get_min_valid_config()
        config2["title"] = "different chall title"
        validator = CTFValidator({}, [config1, config2], ["", ""])

        success, errors = validator.validate()

        assert success
        assert not any([error["code"] == "B006" for error in errors])

    def test_invalid(self):
        config1 = get_min_valid_config()
        config1["title"] = "chall title"

        config2 = get_min_valid_config()
        config2["title"] = "chall title"
        validator = CTFValidator({}, [config1, config2], ["", ""])

        success, errors = validator.validate()

        assert success
        assert any([error["code"] == "B006" for error in errors])


class Test_B007:
    def test_valid(self):
        config1 = get_min_valid_config()
        config1["flags"] = [{"type": "text", "flag": "f14g"}]

        config2 = get_min_valid_config()
        config2["flags"] = [{"type": "text", "flag": "d1ff3r3nt_f14g"}]
        validator = CTFValidator({}, [config1, config2], ["", ""])

        success, errors = validator.validate()

        assert success
        assert not any([error["code"] == "B007" for error in errors])

    def test_invalid(self):
        config1 = get_min_valid_config()
        config1["flags"] = [{"type": "text", "flag": "f14g"}]

        config2 = get_min_valid_config()
        config2["flags"] = [{"type": "text", "flag": "f14g"}]
        validator = CTFValidator({}, [config1, config2], ["", ""])

        success, errors = validator.validate()

        assert success
        assert any([error["code"] == "B007" for error in errors])
