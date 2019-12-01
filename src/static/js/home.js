
$("#incomeSubmit").on("click", ()=>{
    var income_date = moment().format("YYYY-MM-DD");
    var income_type = $( "#incomeSelect option:selected" ).text();
    var income_explanation = $("#incomeExplanation").val();
    var income_price = $("#incomePrice").val();
    income_data = {
        income_date: income_date,
        income_type: income_type,
        income_explanation: income_explanation,
        income_price: income_price
    }

    $.ajax({
        type: "POST",
        url: "/add_income",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify(income_data),
        success: (res)=>{
            console.log(res)
        }
    })
})

function validate(evt) {
    var theEvent = evt || window.event;
  
    // Handle paste
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
    // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }

$("#expenseSubmit").on("click", ()=>{
    var expense_date = moment().format("YYYY-MM-DD");
    var expense_type = $( "#expenseSelect option:selected" ).text();
    var expense_explanation = $("#expenseExplanation").val();
    var expense_price = $("#expensePrice").val();
    expense_data = {
        expense_date: expense_date,
        expense_type: expense_type,
        expense_explanation: expense_explanation,
        expense_price: expense_price
    }
    console.log(expense_data)
    $.ajax({
        type: "POST",
        url: "/add_expense",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify(expense_data),
        success: (res)=>{
            console.log(res)
        }
    })
})