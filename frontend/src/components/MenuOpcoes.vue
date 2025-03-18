<script></script>
<template>
  <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet" />
  <link href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" rel="stylesheet" />

  <input type="checkbox" id="check" />

  <label for="check">
    <i class="fas fa-bars" id="btn">Menu</i>
    <i class="fas fa-times" id="cancel">Fechar</i>
  </label>

  <div class="sidebar">
    <header>Menu</header>

    <a class="link-sidebar active">
      <i class="fas fa-qrcode"></i>
      <span>Profissionais</span>
    </a>

    <a class="link-sidebar">
      <i class="fas fa-link"></i>
      <span>Registros</span>
    </a>

    <a class="link-sidebar">
      <i class="fas fa-edit"></i>
      <span>Turnos</span>
    </a>

    <a class="link-sidebar">
      <i class="far fa-question-circle"></i>
      <span>Registrar</span>
    </a>

    <a class="link-sidebar">
      <i class="fas fa-sliders-h"></i>
      <span>Serviços</span>
    </a>

    <a href="confg06" class="link-sidebar">
      <i class="far fa-envelope"></i>
      <span>Configurações</span>
    </a>
  </div>
</template>

<style scoped>
:root {
  --accent-color: #fff;
  --gradient-color: #fbfbfb;
}

.sidebar {
  position: fixed;
  z-index: 999;
  width: 240px;
  left: -240px;
  height: 100%;
  background-color: #202020;
  transition: all 0.5s ease;
}

.sidebar header {
  font-size: 28px;
  color: #ffffff;
  line-height: 70px;
  text-align: center;
  background-color: #202020;
  user-select: none;
  font-family: 'Lato', sans-serif;
}

.sidebar .link-sidebar {
  display: block;
  height: 65px;
  width: 100%;
  color: #ffffff;
  line-height: 65px;
  padding-left: 30px;
  box-sizing: border-box;
  border-left: 5px solid transparent;
  font-family: 'Lato', sans-serif;
  text-decoration: none;
  transition: all 0.5s ease;
}

.link-sidebar.active,
.link-sidebar:hover {
  border-left: 5px solid var(--accent-color);
  color: #fff;
  background: linear-gradient(to left, var(--accent-color), var(--gradient-color));
}

.sidebar .link-sidebar i {
  font-size: 23px;
  margin-right: 16px;
}

.sidebar .link-sidebar span {
  letter-spacing: 1px;
  text-transform: uppercase;
}

#check {
  display: none;
}

label #btn,
label #cancel {
  position: fixed;
  z-index: 999;
  left: 5px;
  cursor: pointer;
  color: #ffffff;
  border-radius: 50px;
  margin: 15px 30px;
  margin-left: 30px;
  font-size: 22px;
  background-color: #202020;
  height: 45px;
  width: 7vw;
  text-align: center;
  line-height: 44px;
  transition: all 0.5s ease;
}

label #cancel {
  opacity: 0;
  visibility: hidden;
}

#check:checked ~ .sidebar {
  left: 0;
}

#check:checked ~ label #btn {
  margin-left: 245px;
  opacity: 0;
  visibility: hidden;
}

#check:checked ~ label #cancel {
  margin-left: 245px;
  opacity: 1;
  visibility: visible;
}

@media (max-width: 860px) {
  .sidebar {
    height: auto;
    width: 70px;
    left: 0;
    margin: 100px 0;
  }

  header,
  #btn,
  #cancel {
    display: none;
  }

  span {
    position: absolute;
    margin-left: 23px;
    opacity: 0;
    visibility: hidden;
  }

  .sidebar .link-sidebar {
    height: 60px;
  }

  .sidebar .link-sidebar i {
    margin-left: -10px;
  }

  .link-sidebar:hover {
    width: 200px;
    background: inherit;
  }

  .sidebar .link-sidebar:hover span {
    opacity: 1;
    visibility: visible;
  }
}

.sidebar > .link-sidebar.active,
.sidebar > .link-sidebar:hover {
  --accent-color: #32d7fd;
  --gradient-color: #006bdc;
}
</style>
