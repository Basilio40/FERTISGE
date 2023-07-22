$(function() {
  // Ao carregar a página, mostre o conteúdo da primeira guia e adicione a classe "active" a ela
  $("#tabs > div:first-child").addClass("active");

  // Manipule o clique nas guias
  $("#tabs ul li a").click(function(event) {
    event.preventDefault();

    // Remova a classe "active" de todas as guias e oculte todos os conteúdos das guias
    $("#tabs ul li a").removeClass("active");
    $("#tabs > div").removeClass("active");

    // Adicione a classe "active" à guia clicada e mostre o conteúdo correspondente
    $(this).addClass("active");
    $($(this).attr("href")).addClass("active");
  });
});