import allure
import pytest

class Test_Web:
    @allure.title('Test 01: Verify Login')
    @allure.description("This test Verify Successful login to DIA")
    @pytest.mark.smoke
    def test_example(self):
        assert True
