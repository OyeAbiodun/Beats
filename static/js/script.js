document.addEventListener('DOMContentLoaded', () => {
    // Background Image Slideshow
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    if (slides.length) { // Check if slides are present
        const showSlide = (index) => {
            slides.forEach((slide, i) => {
                slide.classList.remove('active');
                if (i === index) {
                    slide.classList.add('active');
                }
            });
        };

        const changeSlide = () => {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        };

        showSlide(currentSlide);
        setInterval(changeSlide, 3000);
    }

    // Dynamic country-state-city selection
    const countrySelect = document.getElementById('country');
    const stateSelect = document.getElementById('state');
    const citySelect = document.getElementById('city');

    if (countrySelect && stateSelect && citySelect) { // Check if selects are present
        fetch('https://api.countrystatecity.in/v1/countries', {
            headers: {
                'X-CSCAPI-KEY': 'NHhvOEcyWk50N2Vna3VFTE00bFp3MjFKR0ZEOUhkZlg4RTk1MlJlaA==' // Replace with your API key
            }
        })
        .then(response => response.json())
        .then(data => {
            data.forEach(country => {
                const option = document.createElement('option');
                option.value = country.iso2;
                option.textContent = country.name;
                countrySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading countries:', error));

        countrySelect.addEventListener('change', function() {
            const countryCode = this.value;
            stateSelect.innerHTML = '<option value="">Select State</option>';
            citySelect.innerHTML = '<option value="">Select City</option>';

            if (countryCode) {
                fetch(`https://api.countrystatecity.in/v1/countries/${countryCode}/states`, {
                    headers: {
                        'X-CSCAPI-KEY': 'NHhvOEcyWk50N2Vna3VFTE00bFp3MjFKR0ZEOUhkZlg4RTk1MlJlaA=='
                    }
                })
                .then(response => response.json())
                .then(data => {
                    data.forEach(state => {
                        const option = document.createElement('option');
                        option.value = state.iso2;
                        option.textContent = state.name;
                        stateSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error loading states:', error));
            }
        });

        stateSelect.addEventListener('change', function() {
            const countryCode = countrySelect.value;
            const stateCode = this.value;
            citySelect.innerHTML = '<option value="">Select City</option>';

            if (stateCode && countryCode) {
                fetch(`https://api.countrystatecity.in/v1/countries/${countryCode}/states/${stateCode}/cities`, {
                    headers: {
                        'X-CSCAPI-KEY': 'NHhvOEcyWk50N2Vna3VFTE00bFp3MjFKR0ZEOUhkZlg4RTk1MlJlaA=='
                    }
                })
                .then(response => response.json())
                .then(data => {
                    data.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city.name;
                        option.textContent = city.name;
                        citySelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error loading cities:', error));
            }
        });
    }
});
