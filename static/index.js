function expand(content,heading,text) {

			var expandContent = document.getElementById(content);
			var contentClass = document.getElementsByClassName('expander-invisible');


			if (expandContent.className != 'expander-visible'){

				expandContent.setAttribute('class', 'expander-visible'); //Show Div

			} else {

				expandContent.setAttribute('class', 'expander-invisible'); //Hide Div

			}

  var expandHeading = document.getElementById(heading);
			var headingClass = document.getElementsByClassName('expander-content-collapsed');

			if (expandHeading.className != 'expander-content-expanded'){

				expandHeading.setAttribute('class', 'expander-content-expanded'); //Show Div

			} else {

				expandHeading.setAttribute('class', 'expander-content-collapsed'); //Hide Div

			}

  var expandText = document.getElementById(text);
			var textClass = document.getElementsByClassName('expander-inactive');

			if (expandText.className != 'expander-active'){

				expandText.setAttribute('class', 'expander-active'); //Show Div

			} else {

				expandText.setAttribute('class', 'expander-inactive'); //Hide Div

			}

		}