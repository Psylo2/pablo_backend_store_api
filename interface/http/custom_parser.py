from flask_restful.reqparse import RequestParser


class CustomParser(RequestParser):
    def __init__(self):
        super().__init__()

    def add_single_argument(self, _type: type, arg_name: str, required: bool, _help: str) -> None:
        if _type == bool:
            self.add_argument(arg_name, '--feature', required=required, help=_help, action='store_true')
            return

        self.add_argument(arg_name, type=_type, required=required, help=_help)

    def add_multi_arguments(self, _type: type, args_names: tuple, required: bool, _help: str) -> None:
        if _type == bool:
            for arg_name in args_names:
                self.add_argument(arg_name, '--feature', required=required, help=_help, action='store_true')
            return

        for arg_name in args_names:
            self.add_argument(arg_name, type=_type, required=required, help=_help)
