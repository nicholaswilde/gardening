# :seedling: Gardening :open_book: <!-- markdownlint-disable-line MD026 -->

[![ci](https://img.shields.io/github/actions/workflow/status/nicholaswilde/gardening/ci.yaml?label=ci&style=for-the-badge&branch=main)](https://github.com/nicholaswilde/gardening/actions/workflows/ci.yaml)
[![linkcheck](https://img.shields.io/github/actions/workflow/status/nicholaswilde/gardening/linkcheck.yaml?label=linkcheck&style=for-the-badge&branch=main)](https://github.com/nicholaswilde/gardening/actions/workflows/linkcheck.yaml)
[![spellcheck](https://img.shields.io/github/actions/workflow/status/nicholaswilde/gardening/spellcheck.yaml?label=spellcheck&style=for-the-badge&branch=main)](https://github.com/nicholaswilde/gardening/actions/workflows/spellcheck.yaml)
[![task](https://img.shields.io/badge/task-enabled-brightgreen?logo=task&logoColor=white&style=for-the-badge)](https://taskfile.dev/)

Documenting my gardening history

## :map: Backyard Garden Layout

```mermaid
graph TD
    %% Garden Layout - Top View
    subgraph backyardSpace[" "]
        direction LR

        Pot1((Backyard Pot 1<br/>🍃 Mint)) ~~~ Hidden1[" "] ~~~ Hidden2[" "]

        %% First row
        Hidden3[" "] ~~~ Bed1[Raised Bed 1<br/>🌺 Flowers] ~~~ Hidden4[" "]

        %% Second row
        Hidden5[" "] ~~~ Bed2[Raised Bed 2<br/>🌿 Herbs] ~~~  Bed3[Raised Bed 3<br/>🌶️  Peppers & <br/>🍅 Tomatoes]

    end

    %% Interactive routing: Click a node to go to its specific markdown page
    click Bed1 "beds/raised-bed-1/" "Go to Bed 1 Notes"
    click Bed2 "beds/raised-bed-2/" "Go to Bed 2 Notes"
    click Bed3 "beds/raised-bed-3/" "Go to Bed 3 Notes"
    click Pot1 "containers/backyard-pot-1/" "Go to Pot 1 Notes"

    %% Catppuccin Mocha Styling
    style Bed1 fill:#313244,stroke:#cba6f7,stroke-width:2px,rx:5,ry:5,color:#cdd6f4
    style Bed2 fill:#313244,stroke:#cba6f7,stroke-width:2px,rx:5,ry:5,color:#cdd6f4
    style Bed3 fill:#313244,stroke:#cba6f7,stroke-width:2px,rx:5,ry:5,color:#cdd6f4
    style Pot1 fill:#313244,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4
    style backyardSpace fill:transparent,stroke:#585b70,stroke-width:2px,stroke-dasharray: 5 5
    style Hidden1 fill:none,stroke:none
    style Hidden2 fill:none,stroke:none
    style Hidden3 fill:none,stroke:none
    style Hidden4 fill:none,stroke:none
    style Hidden5 fill:none,stroke:none
```

## :gear: Development

Development of this site is documented [here][3].

## :scales:​ License

​[Apache 2.0 License](../LICENSE)

## :pencil:​ Author

​This project was started in 2026 by [Nicholas Wilde][2].

[2]: <https://github.com/nicholaswilde/>
[3]: <./reference/development.md>
