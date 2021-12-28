
function onClickedEstimatePrice() {
  var estPrice = document.getElementById("uiEstimatedPrice");
  var url = "http://127.0.0.1:5000/get_predictions";
  var tn_val = document.getElementById("uitown").value;
  var sn_val = document.getElementById("street_name").value;
  var fm_val = document.getElementById("flat_model").value;
  var fa_val = document.getElementById("floor_area").value;
  var ft_val = document.getElementById("flat_type").value;
  var sr_val = document.getElementById("storey_range").value;
  var rl_val = document.getElementById("remaining_lease").value;
  var estPrice = document.getElementById("uiEstimatedPrice");
  $.post(
    url,
    {'town':tn_val,'floor_area':fa_val,'flat_model':fm_val,'street_name':sn_val,'remaining_lease':rl_val,'flat_type':ft_val,'storey_range':sr_val}
	,
    function (data, status) {
      estPrice.innerHTML =
        "<h2> $" + data.estimated_price.toString() + " </h2>";
    }
  );
}