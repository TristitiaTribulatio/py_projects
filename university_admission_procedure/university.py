class University:
    def __init__(self):
        pass

    @staticmethod
    def stage_2():
        marks = [int(input()) for _ in range(3)]
        average_mark = sum(marks)/len(marks)
        print(f"{average_mark}\n")
        if average_mark >= 60:
            print("Congratulations, you are accepted!")
        else:
            print("We regret to inform you that we will not be able to offer you admission.")

    @staticmethod
    def stage_3():
        num, limit = int(input()), int(input())
        applicants = [input().split() for _ in range(num)]
        sorted_applicants = sorted(applicants, key=lambda y: (-float(y[2]), y[0], y[1]))
        print("Successful applicants.txt:\n")
        [print(f"{sorted_applicants[z][0]} {sorted_applicants[z][1]}") for z in range(limit)]

    def stage_4(self):
        init = self.init_stage("4")
        num, applications, faculties, subjects = init[0], init[1], init[2], init[3]
        s_applications = sorted(applications, key=lambda x: (-float(x[2]), x[0], x[1]))
        for f in range(3):
            faculties = self.filling_out_list_4_5(s_applications, faculties, f, num, 3, 2)
        self.print_stage(faculties)

    def stage_5(self):
        init = self.init_stage("5")
        num, applications, faculties, subjects = init[0], init[1], init[2], init[3]
        for f in range(3):
            for key, value in subjects.items():
                s_applications = sorted(applications, key=lambda x: (-float(x[value]), x[0], x[1]))
                faculties = self.filling_out_list_4_5(s_applications, faculties, f, num, 6, value)
        for key, value in faculties.items():
            faculties[key] = sorted(value, key=lambda z: (-float(z[2]), z[0], z[1]))
        self.print_stage(faculties)

    def stage_6(self):
        init = self.init_stage("6")
        num, applications, faculties, subjects = init[0], init[1], init[2], init[3]
        for f in range(3):
            for key, value in subjects.items():
                s_applications = None
                if key in ["Physics", "Engineering"]:
                    s_applications = sorted(applications, key=lambda x: (-float((float(x[value]) + float(x[4])) / 2),
                                            x[0], x[1]))
                elif key == "Biotech":
                    s_applications = sorted(applications, key=lambda x: (-float((float(x[value]) + float(x[2])) / 2),
                                                                         x[0], x[1]))
                elif key in ["Chemistry", "Mathematics"]:
                    s_applications = sorted(applications, key=lambda x: (-float(x[value]), x[0], x[1]))
                for s in range(len(s_applications)):
                    if len(faculties[s_applications[s][6 + f]]) < num:
                        repeat, mark = list(), None
                        for x in faculties.values():
                            repeat += list(filter(lambda y: s_applications[s][0] in y and s_applications[s][1] in y, x))
                        if not repeat and s_applications[s][7 + f] == key:
                            if key == "Biotech":
                                mark = (float(s_applications[s][value]) + float(s_applications[s][2])) / 2
                            elif key in ["Physics", "Engineering"]:
                                mark = (float(s_applications[s][value]) + float(s_applications[s][4])) / 2
                            elif key in ["Chemistry", "Mathematics"]:
                                mark = float(s_applications[s][value])
                            faculties[s_applications[s][6 + f]].append(
                                [s_applications[s][0], s_applications[s][1], mark])
        for key, value in faculties.items():
            faculties[key] = sorted(value, key=lambda z: (-float(z[2]), z[0], z[1]))
        self.save_to_file(faculties)

    def stage_7(self):
        init = self.init_stage("7")
        num, applications, faculties, subjects = init[0], init[1], init[2], init[3]
        for f in range(3):
            for key, value in subjects.items():
                s_applications = None
                if key in ["Physics", "Engineering"]:
                    s_applications = sorted(applications,
                                            key=lambda x: (-max(float(x[6]), float((float(x[value]) + float(x[4])) / 2)),
                                                           x[0], x[1]))
                elif key == "Biotech":
                    s_applications = sorted(applications,
                                            key=lambda x: (-max(float(x[6]), float((float(x[value]) + float(x[2])) / 2)),
                                                           x[0], x[1]))
                elif key in ["Chemistry", "Mathematics"]:
                    s_applications = sorted(applications, key=lambda x: (-max(float(x[6]), float(x[value])), x[0], x[1]))
                for s in range(len(s_applications)):
                    if len(faculties[s_applications[s][7 + f]]) < num:
                        repeat, mark = list(), None
                        for x in faculties.values():
                            repeat += list(
                                filter(lambda y: s_applications[s][0] in y and s_applications[s][1] in y, x))
                        if not repeat and s_applications[s][7 + f] == key:
                            if key == "Biotech":
                                mark = max((float(s_applications[s][value]) + float(s_applications[s][2])) / 2,
                                           float(s_applications[s][6]))
                            elif key in ["Physics", "Engineering"]:
                                mark = max((float(s_applications[s][value]) + float(s_applications[s][4])) / 2,
                                           float(s_applications[s][6]))
                            elif key in ["Chemistry", "Mathematics"]:
                                mark = max(float(s_applications[s][value]), float(s_applications[s][6]))
                            faculties[s_applications[s][7 + f]].append(
                                [s_applications[s][0], s_applications[s][1], mark])
        for key, value in faculties.items():
            faculties[key] = sorted(value, key=lambda z: (-float(z[2]), z[0], z[1]))
        self.save_to_file(faculties)

    @staticmethod
    def filling_out_list_4_5(s_applications, faculties, f, num, subject, mark):
        for s in range(len(s_applications)):
            if len(faculties[s_applications[s][subject + f]]) < num:
                repeat = list()
                for x in faculties.values():
                    repeat += list(filter(lambda y: [s_applications[s][0],
                                                     s_applications[s][1],
                                                     s_applications[s][mark]] == y, x))
                if not repeat:
                    faculties[s_applications[s][subject + f]].append([s_applications[s][0],
                                                                      s_applications[s][1],
                                                                      s_applications[s][mark]])
        return faculties

    @staticmethod
    def print_stage(faculties):
        for key, value in faculties.items():
            print(key)
            for el in value:
                print(f"{el[0]} {el[1]} {el[2]}")
            print("\n", end="")

    @staticmethod
    def init_stage(stage):
        num, applications = int(input()), list()
        faculties = {"Biotech": [], "Chemistry": [], "Engineering": [], "Mathematics": [], "Physics": []}
        subjects = {"Biotech": 3, "Chemistry": 3, "Engineering": 5, "Mathematics": 4, "Physics": 2}
        with open(f"applicant_list_{stage}.txt") as file:
            for y in file.readlines():
                applications.append(y.split())
        return [num, applications, faculties, subjects]

    @staticmethod
    def save_to_file(faculties):
        for key, value in faculties.items():
            with open(f"{key}.txt", "w", encoding="utf-8") as file:
                string = ""
                for el in value:
                    string += f"{el[0]} {el[1]} {el[2]}\n"
                file.write(string)


def main():
    University()

if __name__ == "__main__":
    main()
