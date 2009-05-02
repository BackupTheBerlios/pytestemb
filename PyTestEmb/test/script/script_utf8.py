# -*- coding: UTF-8 -*-




import pytestemb as test





def test_assert():
    test.assert_true(1==1, "предыстория")

def test_trace():
    test.trace_script("предыстория")
    






if __name__ == "__main__":
    
    
    test.add_test_case(test_assert)
    test.add_test_case(test_trace)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


