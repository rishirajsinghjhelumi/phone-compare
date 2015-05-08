 $(document).ready(function() {
            BindControls();
        });

        function BindControls() {
            var brand = ['ARGENTINA', 
                'AUSTRALIA', 
                'BRAZIL', 
                'BELARUS', 
                'BHUTAN',
                'CHILE', 
                'CAMBODIA', 
                'CANADA', 
                'CHILE', 
                'DENMARK', 
                'DOMINICA'];
			
			var model = ['MI3', 
                'MI4', 
                'XT1033', 
                'REDMI1S', 
                'MOTO-G',
                'MOTO-G2', 
                'CAMBODIA', 
                'CANADA', 
                'CHILE', 
                'DENMARK', 
                'DOMINICA'];
				
			 $('#themodel').autocomplete({
                source: model,
                minLength: 0,
                scroll: true
            }).focus(function() {
                $(this).autocomplete("search", "");
            });
			

            $('#thebrand').autocomplete({
                source: brand,
                minLength: 0,
                scroll: true
            }).focus(function() {
                $(this).autocomplete("search", "");
            });
			
			$(window).resize(function() {
			$(".ui-autocomplete").css('display', 'none');
			
			});
        }
		
		