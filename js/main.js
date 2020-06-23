window.onload = function () {
    console.clear();

    const buttons = Array.from(document.querySelectorAll("button"));

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");
        });
    });

    function Get(path) {
        let r = new XMLHttpRequest();
        r.open('GET', path, true);
        r.onreadystatechange = function () {
            if (r.readyState != 4 || r.status != 200)
                return;
            console.log("Success");
        };
        r.send()
        
    }

    function addClickEventListener(operator) {
        document.querySelector("#"+operator).addEventListener('click', function(event)
        {
            Get('/hk9493/'+operator);
        });   
    }

    addClickEventListener('jouyatou');
    addClickEventListener('shoutou');
    addClickEventListener('tentou');
    addClickEventListener('zentou');

    document.querySelector("#iro").addEventListener('wheel', function(event)
    {
        if (event.deltaY < 0)
        {
            Get('/hk9493/shiroiiro');
            console.log('scrolling up');
        }
        else if (event.deltaY > 0)
        {
            Get('/hk9493/atatakaiiro');
            console.log('scrolling down');
        }
    });

    document.querySelector("#akarusa").addEventListener('wheel', function(event)
    {
        if (event.deltaY < 0)
        {
            Get('/hk9493/akarui');
        }
        else if (event.deltaY > 0)
        {
            Get('/hk9493/kurai');
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

