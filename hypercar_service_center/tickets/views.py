from django.views import View
from django.shortcuts import render, redirect

line_of_cars, c_ticket, processed = {"Change oil": [], "Inflate tires": [], "Diagnostic": []}, 0, []


class MenuView(View):
    @staticmethod
    def get(request):
        return render(request, "menu.html", {})


class TicketView(View):
    @staticmethod
    def get(request, service):
        global line_of_cars, c_ticket
        oil_time, tire_time, diagnostic_time, c_wait = 2, 5, 30, None
        c_ticket += 1
        oil_wait = len(line_of_cars['Change oil']) * oil_time
        tire_wait = len(line_of_cars['Inflate tires']) * tire_time
        diagnostic_wait = len(line_of_cars['Diagnostic']) * diagnostic_time

        if c_ticket == 3:
            if oil_wait:
                c_wait = oil_time
            elif tire_wait:
                c_wait = tire_time
            elif diagnostic_wait:
                c_wait = diagnostic_time
        elif c_ticket > 3:
            c_wait = sum([oil_wait, tire_wait, diagnostic_wait])
        else:
            c_wait = 0

        if "change_oil" in service:
            line_of_cars["Change oil"].append([c_ticket, c_wait])
        elif "inflate_tires" in service:
            line_of_cars["Inflate tires"].append([c_ticket, c_wait])
        elif "diagnostic" in service:
            line_of_cars["Diagnostic"].append([c_ticket, c_wait])
        return render(request, "ticket_queue.html", {"c_ticket": c_ticket, "c_wait": c_wait})


class OperatorView(View):
    @staticmethod
    def get(request):
        return render(request, "operator_menu.html", {"change_oil": len(line_of_cars["Change oil"]),
                                                      "inflate_tires": len(line_of_cars["Inflate tires"]),
                                                      "diagnostic": len(line_of_cars["Diagnostic"])})

    @staticmethod
    def post(request):
        global line_of_cars, processed
        if len(line_of_cars["Change oil"]) > 0:
            processed.append(line_of_cars["Change oil"][0][0])
            del line_of_cars["Change oil"][0]
        elif len(line_of_cars["Inflate tires"]) > 0:
            processed.append(line_of_cars["Inflate tires"][0][0])
            del line_of_cars["Inflate tires"][0]
        elif len(line_of_cars["Diagnostic"]) > 0:
            processed.append(line_of_cars["Diagnostic"][0][0])
            del line_of_cars["Diagnostic"][0]
        return redirect("/next")


class NextView(View):
    global processed

    @staticmethod
    def get(request):
        empty, num_of_ticket = False, 0
        if processed:
            num_of_ticket = processed[-1]
        else:
            empty = True
        return render(request, "next.html", {"empty": empty, "num_of_ticket": num_of_ticket})

