from aiogram.dispatcher.filters.state import State, StatesGroup


class PostersForm(StatesGroup):
    Town = State()
    Type = State()
    Title = State()
    Description = State()
    Place = State()
    DateTime = State()
    Cost = State()
    TelNumber = State()
    Approved = State()


class AdminPassword(StatesGroup):
    Password = State()


class ShowPoster(StatesGroup):
    Town = State()


class ChangePoster(StatesGroup):
    ID = State()
    ChangeData = State()