#Custom Exception module here
import sys # import because it gives the details about exception
import logging # to log the errors messages

def error_message_detail(error:Exception,error_detail:sys)->str:
    """
    Extracts detailed error information including file name, line number, and the error message.

    :param error: The exception that occurred.
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    """
    
    # extract trace back details
    _,_,exc_tb=error_detail.exc_info()
    
    # get the file name where exception occured
    file_name=exc_tb.tb_frame.f_code.co_filename
    
    # create the formatted String with file name
    line_number=exc_tb.tb_lineno
    error_message=f"Error occured in python script : [{file_name}] at line number [{line_number}]: {str(error)}"
    
    # log the error for better tracking
    logging.error(error_message)
    
    return error_message
    
class MyException(Exception):
    """
    Custom exception handling inherits base class as Exception
    """    
    def __init__(self, error_message:str,error_detail:sys):
        """
        initializes with a detailed error message 
        parameters: 
        error_message: message describing error
        error_details: sys module to traceback error
        """
        # call the base class constructor with error message
        super().__init__(error_message)
        
        # formet the detailed error message using error _message _detail function
        self.error_message=error_message_detail(error_message,error_detail)
        
    def __str__(self)->str:
        """
        returns the string representation of the error message
        """
        return self.error_message