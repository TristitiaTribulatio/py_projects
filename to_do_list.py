from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import timedelta, date
from sqlalchemy.orm import sessionmaker


def main():
    db_name, Base = "todo.db", declarative_base()
    engine = create_engine(f'sqlite:///{db_name}?check_same_thread=False')

    class Table(Base):
        __tablename__ = "task"
        id = Column(Integer, primary_key=True)
        task = Column(String)
        deadline = Column(Date, default=date.today())

    Base.metadata.create_all(engine)

    while True:
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks"
              "\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        choice = int(input())
        if choice == 1:
            today_tasks(Table, engine)
        elif choice == 2:
            week_tasks(Table, engine)
        elif choice == 3:
            all_tasks(Table, engine)
        elif choice == 4:
            missed_tasks(Table, engine)
        elif choice == 5:
            enter_task(Table, engine)
        elif choice == 6:
            delete_task(Table, engine)
        elif choice == 0:
            print("\nBye!")
            break


def today_tasks(Table, engine):
    today = date.today()
    print(f"\nToday {today.day} {today.strftime('%b')}:")
    get_tasks(Table, engine, today)
    print("\n", end="")


def week_tasks(Table, engine):
    today = date.today()
    while True:
        print(f"\n{today.strftime('%A')} {today.day} {today.strftime('%b')}:")
        get_tasks(Table, engine, today)
        today += timedelta(days=1)
        if today == date.today() + timedelta(days=7):
            break
    print("\n", end="")


def all_tasks(Table, engine):
    print("\nAll tasks:")
    get_all_tasks(Table, engine)
    print("\n", end="")


def missed_tasks(Table, engine):
    print("\nMissed tasks:")
    session = (sessionmaker(bind=engine))()
    rows = session.query(Table).filter(Table.deadline < date.today()).all()
    if len(rows) >= 1:
        for y in range(len(rows)):
            print(f"{y + 1}. {rows[y].task}. {rows[y].deadline.day} {rows[y].deadline.strftime('%b')}")
    elif len(rows) == 0:
        print("Nothing is missed!")
    print("\n", end="")


def delete_task(Table, engine):
    session = (sessionmaker(bind=engine))()
    rows = session.query(Table).all()
    if len(rows) == 0:
        print("\nNothing to delete!")
    elif len(rows) >= 1:
        print("\nChoose the number of the task you want to delete:")
        get_all_tasks(Table, engine)
        index = int(input())
        session.delete((session.query(Table).order_by(Table.deadline).all())[index-1])
        session.commit()
        print("The task has been deleted!")
    print("\n", end="")


def enter_task(Table, engine):
    task, dl = input("\nEnter task\n"), list(map(int, input("Enter deadline\n").split("-")))
    deadline = date(dl[0], dl[1], dl[2])
    session = (sessionmaker(bind=engine))()
    session.add(Table(task=task, deadline=deadline))
    session.commit()
    print("The task has been added!\n")


def get_tasks(Table, engine, today):
    session = (sessionmaker(bind=engine))()
    rows = session.query(Table).filter(Table.deadline == today).all()
    if len(rows) >= 1:
        for x in range(len(rows)):
            print(f"{x + 1}. {rows[x].task}")
    elif len(rows) == 0:
        print("Nothing to do!")


def get_all_tasks(Table, engine):
    session = (sessionmaker(bind=engine))()
    rows = session.query(Table).order_by(Table.deadline).all()
    for y in range(len(rows)):
        print(f"{y + 1}. {rows[y].task}. {rows[y].deadline.day} {rows[y].deadline.strftime('%b')}")


if __name__ == "__main__":
    main()
