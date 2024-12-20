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
        tdTitle.innerHTML = films[i].title;
        tdYear.innerHTML = films[i].year;
        tdRating.innerHTML = films[i].imdb;

        let editButton = document.createElement("button");
        editButton.innerHTML = "Редактировать";
        editButton.onclick = function () {
          editFilm(films[i].id);
        };

        let delButton = document.createElement("button");
        delButton.innerHTML = "Удалить";
        delButton.onclick = function () {
          deleteFilm(films[i].id, films[i].title_ru);
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

  fetch(`/lab7/rest-api/films/${id}`, { method: "DELETE" })
    .then(function (resp) {
      if (resp.ok) {
        fillFilmList();
        return {};
      }
      return resp.json();
    })
    .then(function (errors) {
      if (errors.error) {
        alert(errors.error);
      }
    });
}

function showModal() {
  document.getElementById("title-ru-error").innerHTML = "";
  document.getElementById("title-error").innerHTML = "";
  document.getElementById("year-error").innerHTML = "";
  document.getElementById("description-error").innerHTML = "";
  document.querySelector("div.modal").style.display = "block";
}

function hideModal() {
  document.querySelector("div.modal").style.display = "none";
}

function cancel() {
  hideModal();
}

function addFilm() {
  document.getElementById("id").value = "";
  document.getElementById("title-ru").value = "";
  document.getElementById("title").value = "";
  document.getElementById("year").value = "";
  document.getElementById("imdb").value = "";
  document.getElementById("description").value = "";
  showModal();
}

function sendFilm() {
  const id = document.getElementById("id").value;
  const film = {
    title: document.getElementById("title").value,
    title_ru: document.getElementById("title-ru").value,
    year: document.getElementById("year").value,
    imdb: document.getElementById("imdb").value,
    description: document.getElementById("description").value,
  };

  const url =
    id === "" ? `/lab7/rest-api/films/` : `/lab7/rest-api/films/${id}`;
  const method = id === "" ? "POST" : "PUT";

  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(film),
  })
    .then(function (resp) {
      if (resp.ok) {
        fillFilmList();
        hideModal();
        return {};
      }
      return resp.json();
    })
    .then(function (errors) {
      if (errors.error) {
        alert(errors.error);
      } else {
        document.getElementById("title-ru-error").innerHTML =
          errors.title_ru || "";
        document.getElementById("title-error").innerHTML = errors.title || "";
        document.getElementById("year-error").innerHTML = errors.year || "";
        document.getElementById("description-error").innerHTML =
          errors.description || "";
      }
    });
}

function editFilm(id) {
  fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
      return data.json();
    })
    .then(function (film) {
      if (film.error) {
        alert(film.error);
        return;
      }
      document.getElementById("id").value = id;
      document.getElementById("title-ru").value = film.title_ru;
      document.getElementById("title").value = film.title;
      document.getElementById("year").value = film.year;
      document.getElementById("imdb").value = film.imdb;
      document.getElementById("description").value = film.description;
      showModal();
    });
}
