from django.shortcuts import render

# tradesimulation/views.py

from django.shortcuts import render


def trade_simulation(request):
    return render(request, 'trade_simulation.html')



def process_form(request):
    if request.method == 'POST':
        ticker = request.POST.get('ticker')
        trade_date = request.POST.get('tradeDate')
        contract_type_1 = request.POST.get('contractType1')
        strike_1 = request.POST.get('strike1')
        expiration_1 = request.POST.get('expiration1')
        contract_type_2 = request.POST.get('contractType2')
        strike_2 = request.POST.get('strike2')
        expiration_2 = request.POST.get('expiration2')
        entry_time_start = request.POST.get('entryTimeStart')
        entry_time_end = request.POST.get('entryTimeEnd')
        exit_time_start = request.POST.get('exitTimeStart')
        exit_time_end = request.POST.get('exitTimeEnd')

        # Now you have retrieved all the form data. You can perform further processing,
        # call existing functions with these parameters, or perform any required actions.

        # For example, print the retrieved data
        print(ticker, trade_date, contract_type_1, strike_1, expiration_1,
              contract_type_2, strike_2, expiration_2, entry_time_start,
              entry_time_end, exit_time_start, exit_time_end)

        # You can return an HTTP response, render a template, or redirect
        # return render(request, 'tradesimulation/result.html', {'data': request.POST})
        # return HttpResponseRedirect('/success/')  # Redirect to a success page

    return render(request, 'tradesimulation.html')  # Render an error page or handle GET requests