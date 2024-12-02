function fillFilmList() {
  fetch("/lab7/rest-api/films/")
    .then(function (data) {
      return data.json();
    })
    .then(function (films) {
      let tbody = document.getElementById("film-list");
      tbody.innerHTML = "";
      for (let i = 0; i < films.length; i++) {
        let tr = document.createElement("tr");

        let tdTitleRus = document.createElement("td");
        let tdTitle = document.createElement("td");
        let tdYear = document.createElement("td");
        let tdRating = document.createElement("td");
        let tdActions = document.createElement("td");

        tdTitleRus.innerHTML = films[i].title_ru;
        tdTitle.innerHTML =
          films[i].title == films[i].title_ru ? "" : films[i].title;
        tdYear.innerHTML = films[i].year;
        tdRating.innerHTML = films[i].IMDB;

        let editButton = document.createElement("button");
        editButton.innerHTML = "Редактировать";

        let delButton = document.createElement("button");
        delButton.innerHTML = "Удалить";
        delButton.onclick = function () {
          deleteFilm(i, films[i].title_ru);
        };

        tdActions.append(editButton);
        tdActions.append(delButton);

        tr.append(tdTitleRus);
        tr.append(tdTitle);
        tr.append(tdYear);
        tr.append(tdRating);
        tr.append(tdActions);

        tbody.append(tr);
      }
    });
}

function deleteFilm(id, title) {
  if (!confirm(`Вы уверены, что хотите удалить фильм "${title}"?`)) return;

  fetch(`/lab7/rest-api/films/${id}`, { method: "DELETE" }).then(function () {
    fillFilmList();
  });
}
