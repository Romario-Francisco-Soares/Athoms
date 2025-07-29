<template>
  <div id="app">
    <header class="header">
      <nav class="nav container">
        <div class="logo">Athoms</div>
        <ul class="nav-links">
          <li><a href="#hero" @click.prevent="scrollTo('hero')">Início</a></li>
          <li><a href="#about" @click.prevent="scrollTo('about')">Sobre</a></li>
          <li><a href="#testimonials" @click.prevent="scrollTo('testimonials')">Depoimentos</a></li>
          <li><a href="#contact" @click.prevent="scrollTo('contact')">Contato</a></li>
        </ul>
      </nav>
    </header>

    <section id="hero" class="hero">
    <div class="hero-image">
      <img
        src="https://images.unsplash.com/photo-1607746882042-944635dfe10e?auto=format&fit=crop&w=1400&q=80"
        alt="Reconhecimento facial no trabalho"
      />
      <div class="hero-text">
        <h1>
          Athoms<br />
          <span>Controle de Ponto com Reconhecimento Facial e IA</span>
        </h1>
        <p>
          Simplifique o registro de ponto dos seus colaboradores com tecnologia de ponta em reconhecimento facial e inteligência artificial.
        </p>
        <button @click="scrollTo('contact')" class="btn-primary">Solicitar Demonstração</button>
      </div>
    </div>
  </section>

    <section id="about" class="about container">
      <h2>Sobre o Athoms</h2>
      <p>
        Athoms é um sistema inovador que usa inteligência artificial para reconhecimento facial, facilitando o controle de ponto, eliminando fraudes e aumentando a eficiência do RH.
      </p>
      <ul>
        <li>Registro automático e preciso</li>
        <li>Relatórios detalhados em tempo real</li>
        <li>Fácil integração com sua equipe</li>
        <li>Interface intuitiva para colaboradores e gestores</li>
      </ul>
    </section>

    <section id="testimonials" class="testimonials container">
      <h2>Depoimentos</h2>
      <div class="cards">
        <article v-for="(item, i) in depoimentos" :key="i" class="card">
          <p class="quote">“{{ item.text }}”</p>
          <p class="author">— {{ item.name }}</p>
        </article>
      </div>
    </section>

    <section id="contact" class="contact container">
      <h2>Fale conosco</h2>
      <form @submit.prevent="enviarFormulario" novalidate>
        <input
          v-model="form.empresa"
          type="text"
          placeholder="Nome da empresa"
          required
        />
        <input
          v-model="form.responsavel"
          type="text"
          placeholder="Nome do responsável"
          required
        />
        <input
          v-model="form.email"
          type="email"
          placeholder="E-mail para contato"
          required
        />
        <textarea
          v-model="form.mensagem"
          rows="5"
          placeholder="Como podemos ajudar?"
          required
        ></textarea>
        <button type="submit" class="btn-primary">Enviar</button>
      </form>
    </section>

    <footer class="footer">
      <div class="container">
        © {{ new Date().getFullYear() }} Athoms. Todos os direitos reservados.
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "AthomsLanding",
  data() {
    return {
      form: {
        empresa: "",
        responsavel: "",
        email: "",
        mensagem: "",
      },
      depoimentos: [
        {
          name: "André Lima",
          text: "Com o Athoms, eliminamos o ponto manual e ganhamos transparência com a equipe. Recomendamos fortemente!",
        },
        {
          name: "Carla Mendes",
          text: "A precisão do reconhecimento facial nos impressionou. Simples, seguro e muito eficiente.",
        },
        {
          name: "Empresa XYZ",
          text: "O suporte da equipe e a agilidade de implementação foram essenciais para nosso RH digital.",
        },
      ],
    };
  },
  methods: {
    scrollTo(sectionId) {
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: "smooth" });
      }
    },
    enviarFormulario() {
      // Aqui você pode integrar com backend ou serviço de email
      alert(`Obrigado, ${this.form.responsavel}! Entraremos em contato.`);
      this.form = { empresa: "", responsavel: "", email: "", mensagem: "" };
    },
  },
};
</script>

<style scoped>
/* Reset básico */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'DM Sans', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #01200d;
  background: #fff;
  line-height: 1.6;
  font-size: 16px;
}

.container {
  width: 90%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 0;
}

/* Header */
.header {
  position: sticky;
  top: 0;
  background: #01200d;
  color: #61f177;
  z-index: 1000;
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.15);
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.logo {
  font-weight: 900;
  font-size: 1.8rem;
  letter-spacing: 2px;
  cursor: default;
  color: #61f177;
  user-select: none;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
}

.nav-links a {
  color: #a5dba9;
  font-weight: 600;
  text-decoration: none;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
  transition: color 0.3s ease;
  cursor: pointer;
}

.nav-links a:hover {
  color: #61f177;
}

/* Hero */
.hero {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2rem;
  padding-top: 4rem;
  padding-bottom: 4rem;
  min-height: 70vh;
}

.hero-content {
  flex: 1 1 350px;
  max-width: 600px;
}

.hero-content h1 {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 1rem;
  line-height: 1.1;
}

.hero-content h1 span {
  color: #61f177;
  font-weight: 700;
}

.hero-content p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  color: #234721dd;
}

.btn-primary {
  background-color: #61f177;
  border: none;
  color: white;
  padding: 0.9rem 2rem;
  font-weight: 700;
  font-size: 1.1rem;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 8px 15px -5px #61f177cc;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #4caf50;
  box-shadow: 0 12px 25px -8px #4caf50cc;
}

/* Imagem hero */
.hero-image {
  flex: 1 1 350px;
  max-width: 600px;
  overflow: hidden;
  border-radius: 1rem;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.hero-image img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.hero-image:hover img {
  transform: scale(1.05);
}

/* Sobre */
.about {
  margin-top: 5rem;
  text-align: center;
  color: #234721cc;
}

.about h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #085001c7;
  font-weight: 800;
}

.about p {
  font-size: 1.2rem;
  max-width: 700px;
  margin: 0 auto 2rem auto;
}

.about ul {
  list-style: none;
  max-width: 700px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.2rem;
  padding: 0;
}

.about ul li {
  background: #e8f7e8cc;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  font-weight: 600;
  color: #056108;
  box-shadow: 0 6px 15px -5px #61f177cc;
  transition: background-color 0.3s ease;
}

.about ul li:hover {
  background: #c0eac0;
}

/* Depoimentos */
.testimonials {
  margin-top: 6rem;
  text-align: center;
  color: #085001c7;
}

.testimonials h2 {
  font-weight: 800;
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

.cards {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.card {
  background: #f6fcf6;
  padding: 1.8rem 1.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 10px 30px -10px #7dda7d99;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px -5px #61f177cc;
}

.quote {
  font-style: italic;
  color: #145214;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.author {
  text-align: right;
  font-weight: 700;
  color: #056108;
}

/* Contato */
.contact {
  margin-top: 6rem;
  text-align: center;
  color: #234721cc;
}

.contact h2 {
  font-weight: 800;
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

form {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

input,
textarea {
  padding: 0.9rem 1.2rem;
  border-radius: 1rem;
  border: 2px solid #cbe8cb;
  font-size: 1rem;
  font-weight: 500;
  color: #234721cc;
  transition: all 0.3s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #61f177;
  background: #ebf9eb;
  box-shadow: 0 0 10px #61f17788;
}

textarea {
  resize: vertical;
  min-height: 120px;
}

button[type="submit"] {
  background-color: #61f177;
  border: none;
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
  padding: 1rem 0;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 8px 20px -6px #61f177cc;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #4caf50;
  box-shadow: 0 12px 30px -8px #4caf50cc;
}

/* Footer */
.footer {
  margin-top: 8rem;
  padding: 1.5rem 0;
  background: #01200d;
  color: #a5dba9;
  font-size: 0.9rem;
  text-align: center;
  user-select: none;
}

/* Responsive */
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
  }

  .hero-content h1 {
    font-size: 2.2rem;
  }

  .nav-links {
    gap: 1rem;
  }
}

.hero {
  position: relative;
  width: 100%;
  height: 100vh; /* ocupa toda a altura da viewport */
  overflow: hidden;
}

.hero-image {
  position: relative;
  width: 100%;
  height: 100%;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.6);
  transition: transform 0.4s ease;
}

.hero-image:hover img {
  transform: scale(1.05);
}

/* Overlay de texto sobre a imagem */
.hero-text {
  position: absolute;
  top: 50%;
  left: 8%;
  transform: translateY(-50%);
  max-width: 600px;
  color: #d4f7d4;
  text-shadow:
    2px 2px 6px rgba(0, 0, 0, 0.8),
    0 0 10px rgba(0, 0, 0, 0.5);
}

.hero-text h1 {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1rem;
}

.hero-text h1 span {
  color: #a7f7a7;
  font-weight: 700;
}

.hero-text p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  line-height: 1.4;
  max-width: 450px;
  color: #c6f3c6;
}

.btn-primary {
  background-color: #61f177;
  border: none;
  color: #01200d;
  font-weight: 700;
  font-size: 1.1rem;
  padding: 0.9rem 2.5rem;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 8px 15px -5px #61f177cc;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #4caf50;
  box-shadow: 0 12px 25px -8px #4caf50cc;
}

/* Responsividade */
@media (max-width: 768px) {
  .hero-text {
    position: static;
    transform: none;
    max-width: 100%;
    padding: 2rem 1rem;
    background: rgba(1, 32, 13, 0.6);
    margin-top: -10rem;
    color: #d4f7d4;
    text-align: center;
  }

  .hero-text h1 {
    font-size: 2rem;
  }

  .hero-text p {
    max-width: 100%;
    font-size: 1rem;
  }
}
</style>
