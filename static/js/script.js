// ======================================
// AI CREDIT BANK
// Premium JavaScript
// ======================================

document.addEventListener("DOMContentLoaded", () => {

    /* ======================================
       LOADER
    ====================================== */

    const loader = document.getElementById("loader");

    window.addEventListener("load", () => {

        setTimeout(() => {

            loader.classList.add("hide");

        }, 1500);

    });


    /* ======================================
       SMOOTH SCROLL
    ====================================== */

    document.querySelectorAll('a[href^="#"]').forEach(link => {

        link.addEventListener("click", e => {

            e.preventDefault();

            const target = document.querySelector(link.getAttribute("href"));

            if(target){

                target.scrollIntoView({

                    behavior:"smooth"

                });

            }

        });

    });


    /* ======================================
       NAVBAR SCROLL EFFECT
    ====================================== */

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {

        if(window.scrollY > 80){

            navbar.classList.add("scrolled");

        }

        else{

            navbar.classList.remove("scrolled");

        }

    });


    /* ======================================
       ACTIVE NAVIGATION
    ====================================== */

    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-links a");

    window.addEventListener("scroll", () => {

        let current = "";

        sections.forEach(section => {

            const top = section.offsetTop - 120;

            if(window.scrollY >= top){

                current = section.getAttribute("id");

            }

        });

        navLinks.forEach(link => {

            link.classList.remove("active");

            if(link.getAttribute("href") === "#" + current){

                link.classList.add("active");

            }

        });

    });


    /* ======================================
       HERO CARD TILT
    ====================================== */

    const card = document.querySelector(".credit-card");

    if(card){

        card.addEventListener("mousemove", e => {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;

            const y = e.clientY - rect.top;

            const rotateY = (x - rect.width/2)/18;

            const rotateX = -(y - rect.height/2)/18;

           card.style.transition = "transform .15s ease";

card.style.transform = `
    perspective(1800px)
    rotateY(${rotateY}deg)
    rotateX(${rotateX}deg)
    scale(1.03)
`;
        });

        card.addEventListener("mouseleave", () => {

    card.style.transition = "transform .6s ease";

    card.style.transform = `
        perspective(1500px)
        rotateX(0deg)
        rotateY(0deg)
        scale(1)
    `;

});
    }


    /* ======================================
       COUNTER
    ====================================== */

    const counters = document.querySelectorAll(".counter");

    const counterObserver = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if(entry.isIntersecting){

                const counter = entry.target;

                const target = +counter.dataset.target;

                let current = 0;

                const speed = target / 80;

                const update = () => {

                    current += speed;

                    if(current < target){

                        counter.innerText = Math.floor(current);

                        requestAnimationFrame(update);

                    }

                    else{

                        counter.innerText = target;

                    }

                };

                update();

                counterObserver.unobserve(counter);

            }

        });

    });

    counters.forEach(counter => counterObserver.observe(counter));


    /* ======================================
       FADE ON SCROLL
    ====================================== */

    const revealItems = document.querySelectorAll(

        ".stat-card,.prediction-card,.tech-card,.footer"

    );

    const revealObserver = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if(entry.isIntersecting){

                entry.target.classList.add("show");

            }

        });

    },{

        threshold:.15

    });

    revealItems.forEach(item => {

        item.classList.add("hidden");

        revealObserver.observe(item);

    });


    /* ======================================
       BACK TO TOP
    ====================================== */

    const backTop = document.querySelector(".back-to-top");

    if(backTop){

        backTop.addEventListener("click", e => {

            e.preventDefault();

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        });

    }


    /* ======================================
       FORM VALIDATION
    ====================================== */

    const form = document.querySelector(".prediction-form");

    if(form){

        form.addEventListener("submit", e => {

            const fields = form.querySelectorAll("input, select");

            for(const field of fields){

                if(field.value.trim() === ""){

                    alert("Please complete all required fields.");

                    field.focus();

                    e.preventDefault();

                    return;

                }

            }

        });

    }

});