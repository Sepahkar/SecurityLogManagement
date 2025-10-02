""" Sometimes it is necessary to perform an operation on
the inputs of the utility module functions, in order  to
avoid doing  additional, repetitive   and time-consuming
tasks in the backend.
The helper module does exactly that for us."""


class FixUsername:
    # todo complete docs
    """ Some APIs take username as input. In the databases  of  Django  projects  ,
    the username is sometimes registered with the @eit extension (e.rezaee@eit).
    The point is that the user who is using Utility APIs should not know whether
    the desired api accepts the username with the @eit extension or without it ,
    this is the duty of the Utility, not the user.

    This class is created to handle this.
    """

    def __init__(self, username: str, need_eit: bool = False, need_lower_letter: bool = False):
        self.__username = username
        self.__need_lower_letter = need_lower_letter

        if need_eit:
            if not self.__is_eit_exist():
                self.__add_eit()
        else:
            if self.__is_eit_exist():
                self.__remove_eit()

        if self.__need_lower_letter:
            self.__to_lowercase()

    def __is_eit_exist(self):
        if self.__username.find("@eit") == -1:
            return False
        return True

    def __remove_eit(self):
        self.__username = self.__username.replace("@eit", "")

    def __add_eit(self):
        self.__username += "@eit"

    def __to_lowercase(self):
        self.__username = self.__username.lower()

    @property
    def username(self):
        return self.__username
