window.onload = function () {
    console.clear();

    const buttons = Array.from(document.querySelectorAll("button"));

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");
        });
    });

    document.querySelector("#iro").addEventListener('wheel', function(event)
    {
        if (event.deltaY < 0)
        {
            console.log('scrolling up');
        }
        else if (event.deltaY > 0)
        {
            console.log('scrolling down');
        }
    });

    document.querySelector("#akarusa").addEventListener('wheel', function(event)
    {
        if (event.deltaY < 0)
        {
            console.log('scrolling up');
        }
        else if (event.deltaY > 0)
        {
            console.log('scrolling down');
        }
    });

    // window.addEventListener('wheel', function(event)
    // {
    //     if (event.deltaY < 0)
    //     {
    //         console.log('scrolling up');
    //     }
    //     else if (event.deltaY > 0)
    //     {
    //         console.log('scrolling down');
    //     }
    // });
};

