
$("#incomeSubmit").on("click", ()=>{
    var income_date = moment().format("YYYY-MM-DD");
    var income_type = $( "#incomeSelect option:selected" ).text();
    var income_explanation = $("#incomeExplanation").val();
    var income_price = $("#incomePrice").val();

    if (!income_price || income_price == null || income_price == undefined){
        $("#incomePrice").addClass("notValid")
    }
    if(!income_explanation ){
        $("#incomeExplanation").addClass("notValid")
    }
    if(income_type=="Gelir Seç"){
        $("#incomeSelect").addClass("notValid")
    }

    if(!income_price || !income_type || !income_explanation ){
        return false;
    }

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
            $(".alert").removeClass("none")
            $("#alertText").text("Gelir Eklendi.")
            $("#incomeCancel").click()
            setInterval(function () {
                $(".alert").removeClass("none")
            }, 3000)
        }
    })
})

$("#expenseSubmit").on("click", ()=>{
    var expense_date = moment().format("YYYY-MM-DD");
    var expense_type = $( "#expenseSelect option:selected" ).text();
    var expense_explanation = $("#expenseExplanation").val();
    var expense_price = $("#expensePrice").val();
    
    if (!expense_price || expense_price == null || expense_price == undefined){
        $("#expensePrice").addClass("notValid")
    }
    if(!expense_explanation ){
        $("#expenseExplanation").addClass("notValid")
    }
    if(expense_type=="Gider Seç"){
        $("#expenseSelect").addClass("notValid")
    }

    if(!expense_price || !expense_type || !expense_explanation ){
        return false;
    }
    
    expense_data = {
        expense_date: expense_date,
        expense_type: expense_type,
        expense_explanation: expense_explanation,
        expense_price: expense_price
    }

    $.ajax({
        type: "POST",
        url: "/add_expense",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify(expense_data),
        success: (res)=>{
            $(".alert").removeClass("none")
            $("#alertText").text("Gider Eklendi.")
            $("#expenseCancel").click()
            setInterval(function () {
                $(".alert").removeClass("none")
            }, 3000)
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

    $("#incomeSelect").on("change", ()=>{
        $("#incomeSelect").removeClass("notValid")
    })
    $("#incomeExplanation").on("change", ()=>{
        $("#incomeExplanation").removeClass("notValid")
    })
    $("#incomePrice").on("change", ()=>{
        $("#incomePrice").removeClass("notValid")
    })

    $("#expenseSelect").on("change", ()=>{
        $("#expenseSelect").removeClass("notValid")
    })
    $("#expenseExplanation").on("change", ()=>{
        $("#expenseExplanation").removeClass("notValid")
    })
    $("#expensePrice").on("change", ()=>{
        $("#expensePrice").removeClass("notValid")
    })