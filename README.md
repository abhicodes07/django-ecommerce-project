# 🌱Part 1

- [ ] Getting started with Django
- [ ] Models & Admin
- [ ] Testing -> Models
- [ ] URL's Views
- [ ] Templates -> Tailwind
- [ ] Testing -> Views
- [ ] PEP8 & FLAKE8 - Python style conventions

## 🌿Testing using coverage

- Running tests using `coverage` and excluding `venv` directory

```bash
 coverage run --omit='*/venv/*' manage.py test
```

- Return a HTML results of the test:

```bash
coverage html
```

this creates a `htmlcov` directory containing the `index.html` as a result for the tests.

- Accessing `coverage` HTML output (linux):

```bash
# in root dir
cd htmlcov && explorer.exe index.html
```

# 📝Todos

- Read `unittest` library

# Theme

| Shade          | Hex       | Usage Suggestion          | RGBA                     |
| -------------- | --------- | ------------------------- | ------------------------ |
| `warmgold-100` | `#fff9ed` | Lightest background       | `rgba(255, 249, 237, 1)` |
| `warmgold-200` | `#fdf2dc` | Light cream               | `rgba(253, 242, 220, 1)` |
| `warmgold-300` | `#f5e6c8` | Main (`--color-warmgold`) | `rgba(245, 230, 200, 1)` |
| `warmgold-400` | `#e4d3af` | Hover shade               | `rgba(228, 211, 175, 1)` |
| `warmgold-500` | `#d2be97` | Secondary                 | `rgba(210, 190, 151, 1)` |
| `warmgold-600` | `#bfa97e` | Text, icon, button bg     | `rgba(191, 169, 126, 1)` |
| `warmgold-700` | `#9e8c66` | Accent border             | `rgba(158, 140, 102, 1)` |
| `warmgold-800` | `#7c6f4e` | Deep tone                 | `rgba(124, 111, 78, 1)`  |
| `warmgold-900` | `#5a5237` | Strong contrast/dark mode | `rgba(90, 82, 55, 1)`    |

| Shade           | Hex       | Usage Suggestion               | RGBA                     |
| --------------- | --------- | ------------------------------ | ------------------------ |
| `warmcream-100` | `#f8f6f2` | Ultra light bg                 | `rgba(248, 246, 242, 1)` |
| `warmcream-200` | `#f0ece6` | Light bg                       | `rgba(240, 236, 230, 1)` |
| `warmcream-300` | `#e5e0d8` | Main (`--color-warmcream`)     | `rgba(229, 224, 216, 1)` |
| `warmcream-400` | `#d6d0c6` | Hover shade                    | `rgba(214, 208, 198, 1)` |
| `warmcream-500` | `#bfb9ab` | Text/Icon                      | `rgba(191, 185, 171, 1)` |
| `warmcream-600` | `#a79f94` | Deep hover or border           | `rgba(167, 159, 148, 1)` |
| `warmcream-700` | `#8d867d` | Contrast text                  | `rgba(141, 134, 125, 1)` |
| `warmcream-800` | `#726c65` | Outline/shadow                 | `rgba(114, 108, 101, 1)` |
| `warmcream-900` | `#59524e` | Strong contrast, dark mode use | `rgba(89, 82, 78, 1)`    |

| Shade           | Hex       | Usage Suggestion                | RGBA                     |
| --------------- | --------- | ------------------------------- | ------------------------ |
| `sandstone-100` | `#f3eee7` | Light bg                        | `rgba(243, 238, 231, 1)` |
| `sandstone-200` | `#e5dbcb` | Soft section bg                 | `rgba(229, 219, 203, 1)` |
| `sandstone-300` | `#d6c9b5` | Main (`--color-mildsandstone`)  | `rgba(214, 201, 181, 1)` |
| `sandstone-400` | `#c3b59f` | Hover                           | `rgba(195, 181, 159, 1)` |
| `sandstone-500` | `#b09e88` | Text color                      | `rgba(176, 158, 136, 1)` |
| `sandstone-600` | `#9c8771` | Darker icon or text             | `rgba(156, 135, 113, 1)` |
| `sandstone-700` | `#836f5d` | Outline or border               | `rgba(131, 111, 93, 1)`  |
| `sandstone-800` | `#685746` | Dark hover or background        | `rgba(104, 87, 70, 1)`   |
| `sandstone-900` | `#4d4032` | Darkest, for contrast/dark mode | `rgba(77, 64, 50, 1)`    |
